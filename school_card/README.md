# 荆楚理工移动卡登记

一个极简的校园卡/电话卡登记系统，支持多终端远程访问，方便学校管理人员随时随地登记和查询学生信息。

## 功能

- **登录认证** - 管理员账户登录，保护数据安全
- **新增登记** - 登记学生学号、姓名、学院、电话卡号、原手机号、办理状态
- **学生列表** - 查看所有已登记学生，支持按学号/姓名/学院/卡号/原手机号/状态搜索
- **编辑/删除** - 修改学生信息或删除记录
- **快捷改状态** - 在列表页直接下拉修改办理状态
- **统计看板** - 各办理状态分布、各学院人数排行
- **移动端适配** - 手机浏览器也可正常使用

## 技术栈

- **后端**: Python 3 + Flask 3.x
- **数据库**: SQLite（通过 SQLAlchemy ORM）
- **认证**: Flask-Login + Werkzeug 密码哈希
- **前端**: 纯 HTML + CSS + JavaScript（移动端响应式设计）
- **部署**: PythonAnywhere 免费版

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 初始化数据库（创建管理员账号）
python init_db.py

# 启动服务
python app.py
```

浏览器访问 `http://localhost:5000` 即可。

## 目录结构

```
school_card/
├── app.py              # 应用入口
├── config.py           # 配置（学院列表、状态枚举、数据库路径）
├── models.py           # 数据模型（User, Student）
├── forms.py            # 表单验证
├── init_db.py          # 数据库初始化脚本
├── requirements.txt    # Python 依赖
├── DEPLOY.md           # PythonAnywhere 部署指南
├── routes/
│   ├── __init__.py
│   ├── auth.py         # 登录/登出
│   ├── students.py     # 学生 CRUD
│   └── stats.py        # 统计
├── templates/
│   ├── base.html       # 基础布局
│   ├── login.html      # 登录页
│   ├── index.html      # 学生列表
│   ├── add.html        # 新增登记
│   ├── edit.html       # 编辑登记
│   └── stats.html      # 统计看板
└── static/
    └── style.css       # 样式
```

## 部署到 PythonAnywhere

详细部署步骤见 [DEPLOY.md](DEPLOY.md)。