from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from models import db, Student
from forms import StudentForm
from config import Config

students_bp = Blueprint("students", __name__)


@students_bp.route("/")
@login_required
def index():
    search = request.args.get("search", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 20

    query = Student.query

    if search:
        query = query.filter(
            or_(
                Student.student_id.contains(search),
                Student.name.contains(search),
                Student.college.contains(search),
                Student.phone_card_number.contains(search),
                Student.original_phone.contains(search),
                Student.status.contains(search),
            )
        )

    pagination = query.order_by(Student.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    students = pagination.items

    return render_template(
        "index.html",
        students=students,
        pagination=pagination,
        search=search,
    )


@students_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(
            student_id=form.student_id.data.strip(),
            name=form.name.data.strip(),
            college=form.college.data,
            phone_card_number=form.phone_card_number.data.strip(),
            original_phone=form.original_phone.data.strip(),
            status=form.status.data,
        )
        db.session.add(student)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            if db.session.query(Student.id).filter(
                Student.student_id == form.student_id.data.strip()
            ).first():
                flash("该学号已被登记，请勿重复添加！", "danger")
            else:
                flash("该电话卡号已被登记，请勿重复添加！", "danger")
            return render_template("add.html", form=form)
        flash("学生登记成功！", "success")
        return redirect(url_for("students.index"))
    return render_template("add.html", form=form)


@students_bp.route("/edit/<int:student_id>", methods=["GET", "POST"])
@login_required
def edit(student_id):
    student = db.session.get(Student, student_id)
    if not student:
        flash("未找到该学生记录", "danger")
        return redirect(url_for("students.index"))

    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.student_id = form.student_id.data.strip()
        student.name = form.name.data.strip()
        student.college = form.college.data
        student.phone_card_number = form.phone_card_number.data.strip()
        student.original_phone = form.original_phone.data.strip()
        student.status = form.status.data
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            if db.session.query(Student.id).filter(
                Student.student_id == form.student_id.data.strip(),
                Student.id != student_id,
            ).first():
                flash("该学号已被其他学生登记！", "danger")
            else:
                flash("该电话卡号已被其他学生登记！", "danger")
            return render_template("edit.html", form=form, student=student)
        flash("学生信息更新成功！", "success")
        return redirect(url_for("students.index"))

    return render_template("edit.html", form=form, student=student)


@students_bp.route("/delete/<int:student_id>", methods=["POST"])
@login_required
def delete(student_id):
    student = db.session.get(Student, student_id)
    if not student:
        flash("未找到该学生记录", "danger")
    else:
        db.session.delete(student)
        db.session.commit()
        flash("学生记录已删除", "success")
    return redirect(url_for("students.index"))


@students_bp.route("/status/<int:student_id>", methods=["POST"])
@login_required
def update_status(student_id):
    student = db.session.get(Student, student_id)
    if not student:
        flash("未找到该学生记录", "danger")
        return redirect(url_for("students.index"))

    new_status = request.form.get("status")
    if new_status in Config.STATUS_CHOICES:
        student.status = new_status
        db.session.commit()
        flash("办理状态已更新", "success")
    else:
        flash("无效的办理状态", "danger")

    return redirect(url_for("students.index"))