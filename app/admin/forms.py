# _*_coding:utf-8_*_

# 创建用户  ：chenzhengwei

# 创建日期  ：2019/3/1 下午3:52
import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError

from app.models import Admin, Tag, Movie, Preview


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
        """该方法的目的是保证account唯一，如果在此提交为修改该字段就会raise"""
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


class MovieForm(FlaskForm):
    """电影表单"""
    title = StringField(
        label='电影名称',
        validators=[
            DataRequired('请输入电影名称')
        ],
        description='电影名称',
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请输入电影名称！"
        }
    )
    url = FileField(
        label='电影文件',
        validators=[
            DataRequired('请上传电影文件')
        ],
        description='电影文件',

    )
    info = TextAreaField(
        label='电影简介',
        validators=[
            DataRequired('请输入电影简介')
        ],
        description='电影简介',
        render_kw={
            "class": "form-control",
            "id": "input_info",
            "placeholder": "请输入电影简介！",
            "rows": 10
        }
    )
    logo = FileField(
        label='电影封面',
        validators=[
            DataRequired('请输入电影封面')
        ],
        description='电影封面',
    )
    star = SelectField(
        label='电影星级',
        validators=[
            DataRequired('请选择电影星级')
        ],
        description='电影星级',
        coerce=int,
        choices=[(1,'1星'),(2,'2星'),(3,'3星'),(4,'4星'),(5,'5星')],
        render_kw={
            "class":"form-control",
        }
    )
    tag_id = SelectField(
        label='电影标签',
        validators=[
            DataRequired('请选择电影标签')
        ],
        description='电影标签',
        coerce=int,
        choices=[(val.id, val.name) for val in Tag.query.all()],
        render_kw={
            "class": "form-control",
        }
    )
    area = StringField(
        label='电影上映地区',
        validators=[
            DataRequired('请输入电影上映地区')
        ],
        description='电影上映地区',
        render_kw={
            "class": "form-control",
            "placeholder": "电影上映地区！"
        }
    )
    length = StringField(
        label="电影片长",
        validators=[
            DataRequired("请输入电影片长！")
        ],
        description="电影片长",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入电影片长！"
        }
    )
    release_time = StringField(
        label="电影上映时间",
        validators=[
            DataRequired("请选择电影上映时间！")
        ],
        description="电影上映时间",
        render_kw={
            "class": "form-control",
            "placeholder": "请选择电影上映时间！",
            "id": "input_release_time"
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )

    def validate_title(self, field):
        title = field.data
        num = Movie.query.filter_by(title=title).count()
        if num > 0:
            raise ValidationError("该电影已存在!")


class PreviewForm(FlaskForm):
    """预告片表单"""
    title = StringField(
        label='预告标题',
        validators=[
            DataRequired("请输入预告标题!")
        ],
        description="预告标题",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入预告标题！"
        }
    )
    logo = FileField(
        label='预告封面',
        validators=[
            DataRequired("请上传预告封面!"),
        ],
        description="预告封面",
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary"
        }
    )

    def validate_title(self,field):
        title = field.data
        num = Preview.query.filter_by(title=title).count()
        if num > 0:
            raise ValidationError('该预告片已存在')