from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

from config import Config


class LoginForm(FlaskForm):
    username = StringField(
        "用户名", validators=[DataRequired(message="请输入用户名"), Length(max=80)]
    )
    password = PasswordField(
        "密码", validators=[DataRequired(message="请输入密码")]
    )
    submit = SubmitField("登录")


class StudentForm(FlaskForm):
    student_id = StringField(
        "学号",
        validators=[
            DataRequired(message="请输入学号"),
            Length(max=30, message="学号不能超过30个字符"),
        ],
    )
    name = StringField(
        "姓名",
        validators=[
            DataRequired(message="请输入学生姓名"),
            Length(max=50, message="姓名不能超过50个字符"),
        ],
    )
    college = SelectField(
        "学院",
        choices=[(c, c) for c in Config.COLLEGES],
        validators=[DataRequired(message="请选择学院")],
    )
    phone_card_number = StringField(
        "电话卡号",
        validators=[
            DataRequired(message="请输入电话卡号"),
            Length(max=50, message="电话卡号不能超过50个字符"),
            Regexp(r"^[A-Za-z0-9\-]+$", message="电话卡号只能包含字母、数字和短横线"),
        ],
    )
    original_phone = StringField(
        "原手机号",
        validators=[
            DataRequired(message="请输入原手机号"),
            Length(min=11, max=11, message="原手机号必须为11位"),
            Regexp(r"^1\d{10}$", message="原手机号格式不正确，请输入11位手机号"),
        ],
    )
    status = SelectField(
        "办理状态",
        choices=[(s, s) for s in Config.STATUS_CHOICES],
        validators=[DataRequired(message="请选择办理状态")],
    )
    submit = SubmitField("保存")