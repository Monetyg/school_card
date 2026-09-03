"""初始化数据库：建表并创建初始管理员账号。

用法：
    python init_db.py
或指定用户名/密码：
    python init_db.py admin 123456
"""
import sys

from werkzeug.security import generate_password_hash

from app import create_app
from models import db, User

app = create_app()


def main():
    username = sys.argv[1] if len(sys.argv) > 1 else input("请输入管理员用户名（默认 admin）：").strip() or "admin"
    password = sys.argv[2] if len(sys.argv) > 2 else input("请输入管理员密码：").strip()
    if not password:
        print("密码不能为空！")
        return

    with app.app_context():
        db.create_all()

        existing = User.query.filter_by(username=username).first()
        if existing:
            # 已存在则更新密码
            existing.password_hash = generate_password_hash(password)
            db.session.commit()
            print(f"用户 {username} 已存在，密码已更新。")
        else:
            user = User(username=username, password_hash=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            print(f"管理员账号 {username} 创建成功。")

        print("数据库初始化完成。")


if __name__ == "__main__":
    main()
