# _*_coding:utf-8_*_

# 创建用户  ：chenzhengwei

# 创建日期  ：2019/3/1 下午3:52

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from app.models import Admin


class LoginForm(FlaskForm):
    """登录表单"""
    account = StringField(
        label='账号',
        validators=[
            DataRequired('请输入管理员账号！')
        ],
        description='账号',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员账号！",
            "required": "required"
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired('请输入管理员密码！')
        ],
        description='密码',
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员密码！",
            "required": "required"
        }
    )
    submit = SubmitField(
        label='登录',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )

    def validate_account(self,field):
        account = field.data
        admin_obj = Admin.query.filter_by(name=account).count()
        if admin_obj == 0:
            raise ValidationError('账户不存在！')


class TagForm(FlaskForm):
    """标签表单"""
    name = StringField(
        label='标签名称',
        validators=[
            DataRequired('请输入标签名称')
        ],
        description='标签名称',
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签名称！"
        }
    )
    submit = SubmitField(
        label='编辑',
        render_kw={
            "class": "btn btn-primary"
        }
    )