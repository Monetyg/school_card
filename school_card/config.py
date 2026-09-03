import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-to-a-random-secret-key")

    # SQLite 数据库文件路径
    # 部署到 PythonAnywhere 时建议改为 ~/school_card.db
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "school_card.db"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 学院固定列表
    COLLEGES = [
        "智能制造学院",
        "新能源学院",
        "化工与制药学院",
        "食品与生物学院",
        "人工智能学院",
        "数理学院",
        "师范学院",
        "文学与传媒学院",
        "艺术学院",
        "经济与管理学院",
        "外国语学院",
    ]

    # 办理状态枚举
    STATUS_CHOICES = ["未办理", "办理中", "已办理", "已激活"]