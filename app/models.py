# _*_coding:utf-8_*_
# 创建用户  ：chenzhengwei
# 创建日期  ：2019/3/1 下午3:52
import datetime
import pymysql

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:chenzwcc@127.0.0.1:3306/movie'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class User(db.Model):
    # 用户
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.Text)
    face = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)
    uuid = db.Column(db.String(255), unique=True)
    userlogs = db.relationship('Userlog', backref='user')  # 绑定用户日志外健关联
    comments = db.relationship('Comment', backref='user')
    moviecols = db.relationship('Moviecol', backref='user')

    def __str__(self):
        return "<User %s>" % self.name


class Userlog(db.Model):
    # 用户日志
    __tablename = 'userlog'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 定义外健
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)

    def __str__(self):
        return "<Userlog %s>" % id


class Tag(db.Model):
    # 标签
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)
    movies = db.relationship('Movie', backref='tag')

    def __str__(self):
        return "<Tag %s>" % self.name


class Movie(db.Model):
    # 电影
    __tablename__ = "movie"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    info = db.Column(db.Text)
    logo = db.Column(db.String(255), unique=True)
    star = db.Column(db.SmallInteger)
    playnum = db.Column(db.BigInteger)
    commentnum = db.Column(db.BigInteger)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))
    area = db.Column(db.String(255))
    release_time = db.Column(db.Date)  # 上映时间
    length = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)
    comments = db.relationship("Comment", backref="movie")
    moviecols = db.relationship("Moviecol", backref="movie")

    def __str__(self):
        return "<Movie %s>" % self.title


class Preview(db.Model):
    # 预告
    __tablename__ = "preview"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)

    def __str__(self):
        return "<Preview %s>" % self.title


class Comment(db.Model):
    # 评论
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)
    content = db.Column(db.Text)

    def __str__(self):
        return "<Comment %s>" % self.id


class Moviecol(db.Model):
    # 电影收藏
    __tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)

    def __str__(self):
        return "<Moviecol %s>" % self.id


class Auth(db.Model):
    # 权限
    __tablename__ = 'auth'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)

    def __str__(self):
        return '<Auth %s>' % self.name


class Role(db.Model):
    # 角色
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    auths = db.Column(db.String(600))  # 权限
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)
    admins = db.relationship('Admin', backref='role')  # 管理员外键关系关联

    def __str__(self):
        return '<Role %s>' % self.name


class Admin(db.Model):
    # 管理员
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    is_super = db.Column(db.Boolean)
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    adminlogs = db.relationship("Adminlog", backref='admin')
    oplogs = db.relationship('Oplog', backref='admin')

    def __str__(self):
        return "<Admin %s>" % self.name


class Adminlog(db.Model):
    # 管理员登录日志
    __tablename__ = 'adminlog'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)

    def __str__(self):
        return "<Adminlog %s>" % self.id


class Oplog(db.Model):
    # 操作日志
    __tablename__ = "oplog"

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now)

    def __str__(self):
        return "<Oplog %s>" % self.id


if __name__ == '__main__':
    db.create_all() # 执行该命令行自动将数据表设计同步到数据库

    # role = Role(
    #     name="超级管理员",
    #     auths=""
    # )
    # db.session.add(role)
    # db.session.commit()

    # from werkzeug.security import generate_password_hash
    #
    # admin = Admin(
    #     name="chenzwcc",
    #     pwd=generate_password_hash('admin123'),
    #     is_super=True,
    #     role_id=1
    # )
    # db.session.add(admin)
    # db.session.commit()
