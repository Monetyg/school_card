# 校园卡/电话卡登记系统 - 部署指南 (PythonAnywhere)

## 一、本地运行（开发调试）

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 初始化数据库（创建表 + 管理员账号）
python init_db.py

# 3. 启动开发服务器
python app.py
```

浏览器访问 `http://localhost:5000`，使用刚创建的管理员账号登录。

---

## 二、部署到 PythonAnywhere（免费版）

### 1. 注册账号

访问 https://www.pythonanywhere.com 注册免费账号。

### 2. 上传项目文件

进入 **Dashboard → Files**，在 `/home/你的用户名/` 下创建 `school_card` 目录，
通过网页上传所有项目文件，或者使用 Git 克隆（若你的代码在 GitHub 上）：

```bash
git clone https://github.com/你的用户名/school_card.git
```

### 3. 创建虚拟环境并安装依赖

进入 **Dashboard → Consoles → Bash**：

```bash
cd ~/school_card
mkvirtualenv school_card --python=python3.10
pip install -r requirements.txt
```

### 4. 修改数据库路径（重要）

免费版 Web 应用每次"重载"时，项目目录下的文件不会被删除，但为了数据安全，
建议把数据库文件放在 home 目录下。

编辑 `config.py`，把数据库路径改为：

```python
SQLALCHEMY_DATABASE_URI = "sqlite:////home/你的用户名/school_card.db"
```

> 注意：`sqlite:///` 后是四个斜杠，第四个斜杠是绝对路径的开头。
> 同时建议修改 `SECRET_KEY` 为一段随机字符串。

### 5. 初始化数据库

继续在 Bash 控制台运行：

```bash
cd ~/school_card
python init_db.py admin 你的管理员密码
```

> 如果之后想改密码，再次运行这个命令即可。

### 6. 配置 Web 应用

进入 **Dashboard → Web**：

1. 点击 **Add a new web app**
2. 选择 **Manual configuration**，Python 版本选 **Python 3.10**
3. 在 **Code** 部分点击 **WSGI configuration file**，替换全部内容为：

```python
import sys

project_home = "/home/你的用户名/school_card"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import create_app

application = create_app()
```

4. 在 **Virtualenv** 部分填入：`/home/你的用户名/.virtualenvs/school_card`

### 7. 配置静态文件（可选）

进入 **Static files** 部分，添加：

- URL：`/static/`
- Directory：`/home/你的用户名/school_card/static/`

### 8. 重载应用

点击绿色 **Reload** 按钮。

访问 `https://你的用户名.pythonanywhere.com` 即可使用。

---

## 三、常见问题

### Q: 忘记管理员密码怎么办？

```bash
cd ~/school_card
python init_db.py admin 新密码  
```

### Q: 数据库被重置 / 数据丢失？

- 确认数据库文件路径是 `~` 目录（home）下，而不是项目目录
- 免费版在每月 1 号会重置非 home 目录以外的文件，项目目录下的数据库会丢失

### Q: 免费版配额够用吗？

- 每天 6 小时 CPU 时间，个人登记系统足够
- 512MB 存储，存几万条记录绰绰有余
- 免费版有 3 个 Web 应用名额

### Q: 如何备份数据？

定期下载 home 目录下的 `school_card.db` 文件即可，或者：

```bash
cp ~/school_card.db ~/school_card.db.bak
```
