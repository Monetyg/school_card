from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func

from models import db, Student
from config import Config

stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/stats")
@login_required
def index():
    total = Student.query.count()

    # 各办理状态统计
    status_counts = {}
    for status in Config.STATUS_CHOICES:
        status_counts[status] = Student.query.filter_by(status=status).count()

    # 各学院统计
    college_rows = (
        db.session.query(Student.college, func.count(Student.id).label("count"))
        .group_by(Student.college)
        .order_by(func.count(Student.id).desc())
        .all()
    )
    college_counts = {row.college: row.count for row in college_rows}

    return render_template(
        "stats.html",
        total=total,
        status_counts=status_counts,
        college_counts=college_counts,
        colleges=Config.COLLEGES,
        status_choices=Config.STATUS_CHOICES,
    )