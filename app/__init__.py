# _*_coding:utf-8_*_

# 创建用户  ：chenzhengwei

# 创建日期  ：2019/3/1 下午3:50
import os

from flask import Flask, render_template
import pymysql
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:chenzwcc@127.0.0.1:3306/movie'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY']='123456'
app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/file_uploads/')
app.debug=True

db = SQLAlchemy(app)

from app.admin import admin as admin_blueprint
from app.home import home as home_blueprint

app.register_blueprint(admin_blueprint,url_prefix="/admin")
app.register_blueprint(home_blueprint)


@app.errorhandler(404)
def page_not_found(err):
    return render_template('home/404.html'), 404