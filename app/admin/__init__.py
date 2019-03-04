# _*_coding:utf-8_*_

# 创建用户  ：chenzhengwei

# 创建日期  ：2019/3/1 下午3:51

from flask import Blueprint
admin = Blueprint('admin',__name__)
import app.admin.views

