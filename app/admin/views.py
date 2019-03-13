# _*_coding:utf-8_*_

# 创建用户  ：chenzhengwei

# 创建日期  ：2019/3/1 下午3:52
from flask import render_template, redirect, url_for, flash, session, request
from functools import wraps

from app import db
from app.models import Admin, Tag
from . import admin
from .forms import LoginForm, TagForm


# 装饰器函数：保证为登录的用户不等访问需要登录信息的页面
def admin_login_req(func):
    @wraps(func)
    def decorate_function(*args,**kwargs):
        if session.get('account_name',None) is None:
            print('next',request.url)
            return redirect(url_for('admin.login',next=request.url))
        return func(*args,**kwargs)
    return decorate_function


@admin.route('/')
@admin_login_req
def index():
    return render_template('admin/index.html')


@admin.route('/login/',methods=['GET','POST'])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        data = loginform.data
        admin_obj = Admin.query.filter_by(name=data['account']).first()
        if not admin_obj.check_pwd(data['pwd']):
            flash('密码错误！')
            return redirect(url_for('admin.login'))
        session['account_name'] = data['account']
        return redirect(url_for('admin.index') or request.args.get('next'))
    return render_template('admin/login.html',loginform=loginform)


@admin.route('/logout/')
@admin_login_req
def logout():
    session.clear()
    return redirect(url_for('admin.login'))


@admin.route('/pwd/')
@admin_login_req
def pwd():
    return render_template('admin/pwd.html')


@admin.route('/tag/add/',methods=['GET','POST'])
@admin_login_req
def tag_add():
    tag_form = TagForm()
    if tag_form.validate_on_submit():
        data = tag_form.data
        tag = Tag.query.filter_by(name=data['name']).count()
        if tag==1:
            flash('标签已经存在！','error')
            return redirect(url_for('admin.tag_add'))
        else:
            tag_obj = Tag(name=data['name'])
            db.session.add(tag_obj)
            db.session.commit()
            flash('标签添加成功！','success')
            return redirect(url_for('admin.tag_list',page=1))
    return render_template('admin/tag_add.html',tag_form=tag_form)


@admin.route('/tag/list/<int:page>')
@admin_login_req
def tag_list(page=1):
    if page<=0:
        page=1
    page_objs = Tag.query.order_by(Tag.addtime.desc()).paginate(page=page,per_page=2)
    return render_template('admin/tag_list.html',page_objs=page_objs)


@admin.route('/tag/edit/<int:id>',methods=['GET','POST'])
@admin_login_req
def tag_edit(id=None):
    tag_form = TagForm()
    tag_obj = Tag.query.get_or_404(id)
    if tag_form.validate_on_submit():
        data = tag_form.data
        tag_count = Tag.query.filter_by(name=data['name']).count()
        if tag_count == 1 and tag_obj.name == data['name']:
            flash('标签已经存在！','error')
            return redirect(url_for('admin.tag_edit',id=id))
        else:
            tag_obj.name = data['name']
            db.session.add(tag_obj)
            db.session.commit()
            flash('标签修改成功！','success')
            return redirect(url_for('admin.tag_list',page=1))

    return render_template('admin/tag_edit.html',tag_form=tag_form,tag_obj=tag_obj)


@admin.route('/tag/del/<int:id>',methods=['GET','POST'])
@admin_login_req
def tag_del(id=None):
    tag_obj = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag_obj)
    db.session.commit()
    flash('标签删除成功！','success')
    return redirect(url_for('admin.tag_list',page=1))


@admin.route('/movie/add/')
@admin_login_req
def movie_add():
    return render_template('admin/movie_add.html')


@admin.route('/movie/list/')
@admin_login_req
def movie_list():
    return render_template('admin/movie_list.html')


@admin.route('/preview/add/')
@admin_login_req
def preview_add():
    return render_template('admin/preview_add.html')


@admin.route('/preview/list/')
@admin_login_req
def preview_list():
    return render_template('admin/preview_list.html')


@admin.route('/user/view/')
@admin_login_req
def user_view():
    return render_template('admin/user_view.html')


@admin.route('/user/list/')
@admin_login_req
def user_list():
    return render_template('admin/user_list.html')


@admin.route('/comment/list/')
@admin_login_req
def comment_list():
    return render_template('admin/comment_list.html')


@admin.route('/moviecol/list/')
@admin_login_req
def moviecol_list():
    return render_template('admin/moviecol_list.html')


@admin.route('/oplog/list/')
@admin_login_req
def oplog_list():
    return render_template('admin/oplog_list.html')


@admin.route('/adminloginlog/list/')
@admin_login_req
def adminloginlog_list():
    return render_template('admin/adminloginlog_list.html')


@admin.route('/userloginlog/list/')
@admin_login_req
def userloginlog_list():
    return render_template('admin/userloginlog_list.html')


@admin.route('/auth/add/')
@admin_login_req
def auth_add():
    return render_template('admin/auth_add.html')


@admin.route('/auth/list/')
@admin_login_req
def auth_list():
    return render_template('admin/auth_list.html')


@admin.route('/role/add/')
@admin_login_req
def role_add():
    return render_template('admin/role_add.html')


@admin.route('/role/list/')
@admin_login_req
def role_list():
    return render_template('admin/role_list.html')


@admin.route('/admin/add/')
@admin_login_req
def admin_add():
    return render_template('admin/admin_add.html')


@admin.route('/admin/list/')
@admin_login_req
def admin_list():
    return render_template('admin/admin_list.html')