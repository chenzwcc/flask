# _*_coding:utf-8_*_

# 创建用户  ：chenzhengwei

# 创建日期  ：2019/3/1 下午3:50

from flask import Flask


app = Flask(__name__)
app.debug=True

from app.admin import admin as admin_blueprint
from app.home import home as home_blueprint


app.register_blueprint(admin_blueprint,url_prefix="/admin")
app.register_blueprint(home_blueprint,url_prefix='/home')
