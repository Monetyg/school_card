"""端到端冒烟测试：验证登录、新增、列表、搜索、状态更新、统计全流程。"""
import re
import sys

import requests

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 清理测试数据，保证可重复运行
from app import create_app
from models import db, Student

app = create_app()
with app.app_context():
    Student.query.delete()
    db.session.commit()
    print("[SETUP] 已清空 students 表")

BASE = "http://127.0.0.1:5000"
session = requests.Session()

# 1. 获取登录页（提取 CSRF token + session cookie）
r = session.get(f"{BASE}/auth/login")
assert r.status_code == 200, f"登录页 {r.status_code}"
csrf = re.search(r'name="csrf_token" type="hidden" value="([^"]+)"', r.text)
assert csrf, "未找到 CSRF token"
print("[OK] 登录页可访问")

# 2. 未登录访问 / 应被重定向
r = session.get(f"{BASE}/", allow_redirects=False)
assert r.status_code == 302, f"未登录访问应 302, 实际 {r.status_code}"
print("[OK] 未登录访问被重定向到登录页")

# 3. 错误密码应登录失败
r = session.post(f"{BASE}/auth/login", data={"username": "admin", "password": "wrong", "csrf_token": csrf.group(1)})
assert "用户名或密码错误" in r.text, "错误密码应提示失败"
print("[OK] 错误密码被拒绝")

# 4. 正确登录
r = session.post(f"{BASE}/auth/login", data={"username": "admin", "password": "admin123", "csrf_token": csrf.group(1)})
assert r.status_code == 200 and "学生列表" in r.text or "新增登记" in r.text, "登录后应看到主页"
print("[OK] 管理员登录成功")

# 5. 新增登记
def get_csrf(path):
    r = session.get(f"{BASE}{path}")
    m = re.search(r'name="csrf_token" type="hidden" value="([^"]+)"', r.text)
    assert m, f"{path} 未找到 CSRF"
    return m.group(1)

students = [
    ("20230001", "张三", "人工智能学院", "18912340001", "13812340001", "未办理"),
    ("20230002", "李四", "智能制造学院", "18912340002", "13812340002", "办理中"),
    ("20230003", "王五", "新能源学院", "18912340003", "13812340003", "已办理"),
    ("20230004", "赵六", "师范学院", "18912340004", "13812340004", "已激活"),
    ("20230005", "钱七", "人工智能学院", "18912340005", "13812340005", "已办理"),
]
for sid, name, college, card, original_phone, status in students:
    r = session.post(
        f"{BASE}/add",
        data={"student_id": sid, "name": name, "college": college, "phone_card_number": card, "original_phone": original_phone, "status": status, "csrf_token": get_csrf("/add")},
        allow_redirects=False,
    )
    assert r.status_code == 302, f"新增 {name} 应重定向, 实际 {r.status_code}"
print(f"[OK] 成功登记 {len(students)} 名学生")

# 6. 重复卡号应被拒绝（数据库唯一约束）
r = session.post(
    f"{BASE}/add",
    data={"student_id": "20230006", "name": "重复卡号", "college": "人工智能学院", "phone_card_number": "18912340001", "original_phone": "13812340006", "status": "未办理", "csrf_token": get_csrf("/add")},
)
assert "已被登记" in r.text, "重复卡号应提示已被登记"
print("[OK] 重复卡号被数据库唯一约束拦截")

# 6.1 重复学号应被拒绝（数据库唯一约束）
r = session.post(
    f"{BASE}/add",
    data={"student_id": "20230001", "name": "重复学号", "college": "人工智能学院", "phone_card_number": "18912340007", "original_phone": "13812340007", "status": "未办理", "csrf_token": get_csrf("/add")},
)
assert "学号已被登记" in r.text, "重复学号应提示已被登记"
print("[OK] 重复学号被数据库唯一约束拦截")

# 7. 列表页渲染
r = session.get(f"{BASE}/")
assert r.status_code == 200 and "张三" in r.text and "李四" in r.text
print("[OK] 列表页显示所有已登记学生")

# 8. 搜索
r = session.get(f"{BASE}/", params={"search": "人工智能学院"})
assert "张三" in r.text and "钱七" in r.text and "李四" not in r.text
print("[OK] 按学院搜索正常")

# 9. 编辑学生（改用新卡号避免与其他记录冲突）
student_page = session.get(f"{BASE}/")
m = re.search(r"/edit/(\d+)", student_page.text)
student_id = m.group(1)
r = session.post(
    f"{BASE}/edit/{student_id}",
    data={"student_id": "20230005", "name": "张三丰", "college": "人工智能学院", "phone_card_number": "18912340006", "original_phone": "13812340006", "status": "已激活", "csrf_token": get_csrf(f"/edit/{student_id}")},
    allow_redirects=False,
)
assert r.status_code == 302, f"编辑应重定向, 实际 {r.status_code}"
r = session.get(f"{BASE}/")
assert "张三丰" in r.text
assert "18912340006" in r.text
print("[OK] 编辑学生成功（钱七 -> 张三丰，卡号 18912340006）")

# 10. 快捷修改状态
r = session.post(f"{BASE}/status/{student_id}", data={"status": "办理中"}, allow_redirects=False)
assert r.status_code == 302, f"快捷改状态应重定向, 实际 {r.status_code}"
r = session.get(f"{BASE}/")
assert "办理中" in r.text
print("[OK] 快捷修改状态成功")

# 11. 统计页
r = session.get(f"{BASE}/stats")
assert r.status_code == 200
assert "登记总人数" in r.text
print("[OK] 统计页可访问")

# 12. 删除学生
r = session.post(f"{BASE}/delete/{student_id}", allow_redirects=False)
assert r.status_code == 302
r = session.get(f"{BASE}/")
assert "张三丰" not in r.text
print("[OK] 删除学生成功")

# 13. 登出
r = session.get(f"{BASE}/auth/logout", allow_redirects=False)
assert r.status_code == 302
r = session.get(f"{BASE}/", allow_redirects=False)
assert r.status_code == 302
print("[OK] 登出后无法访问主页")

print("\n全部测试通过 ✓")
