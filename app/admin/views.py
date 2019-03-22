# _*_coding:utf-8_*_

# 创建用户  ：chenzhengwei

# 创建日期  ：2019/3/1 下午3:52
import datetime
import os
import uuid

from flask import render_template, redirect, url_for, flash, session, request
from functools import wraps

from werkzeug.utils import secure_filename

from app import db, app
from app.models import Admin, Tag, Movie, Preview
from . import admin
from .forms import LoginForm, TagForm, MovieForm, PreviewForm


# 装饰器函数：保证为登录的用户不等访问需要登录信息的页面
def admin_login_req(func):
    @wraps(func)
    def decorate_function(*args, **kwargs):
        if session.get('account_name', None) is None:
            return redirect(url_for('admin.login', next=request.url))
        return func(*args, **kwargs)

    return decorate_function


# 对文件进行处理，生成唯一名称并返回
def generate_unique_name(filename):
    file = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + file[-1]
    return filename


@admin.route('/')
@admin_login_req
def index():
    return render_template('admin/index.html')


@admin.route('/login/', methods=['GET', 'POST'])
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
    return render_template('admin/login.html', loginform=loginform)


@admin.route('/logout/')
@admin_login_req
def logout():
    session.clear()
    return redirect(url_for('admin.login'))


@admin.route('/pwd/')
@admin_login_req
def pwd():
    return render_template('admin/pwd.html')


@admin.route('/tag/add/', methods=['GET', 'POST'])
@admin_login_req
def tag_add():
    tag_form = TagForm()
    if tag_form.validate_on_submit():
        data = tag_form.data
        tag = Tag.query.filter_by(name=data['name']).count()
        if tag == 1:
            flash('标签已经存在！', 'error')
            return redirect(url_for('admin.tag_add'))
        else:
            tag_obj = Tag(name=data['name'])
            db.session.add(tag_obj)
            db.session.commit()
            flash('标签添加成功！', 'success')
            return redirect(url_for('admin.tag_list', page=1))
    return render_template('admin/tag_add.html', tag_form=tag_form)


@admin.route('/tag/list/<int:page>')
@admin_login_req
def tag_list(page=1):
    if page <= 0:
        page = 1
    page_objs = Tag.query.order_by(Tag.addtime.desc()).paginate(page=page, per_page=2)
    return render_template('admin/tag_list.html', page_objs=page_objs)


@admin.route('/tag/edit/<int:id>', methods=['GET', 'POST'])
@admin_login_req
def tag_edit(id=None):
    tag_form = TagForm()
    tag_obj = Tag.query.get_or_404(id)
    if tag_form.validate_on_submit():
        data = tag_form.data
        tag_count = Tag.query.filter_by(name=data['name']).count()
        if tag_count == 1 and tag_obj.name == data['name']:
            flash('标签已经存在！', 'error')
            return redirect(url_for('admin.tag_edit', id=id))
        else:
            tag_obj.name = data['name']
            db.session.add(tag_obj)
            db.session.commit()
            flash('标签修改成功！', 'success')
            return redirect(url_for('admin.tag_list', page=1))

    return render_template('admin/tag_edit.html', tag_form=tag_form, tag_obj=tag_obj)


@admin.route('/tag/del/<int:id>', methods=['GET', 'POST'])
@admin_login_req
def tag_del(id=None):
    tag_obj = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag_obj)
    db.session.commit()
    flash('标签删除成功！', 'success')
    return redirect(url_for('admin.tag_list', page=1))


@admin.route('/movie/add/', methods=['GET', 'POST'])
@admin_login_req
def movie_add():
    movie_form = MovieForm()
    if movie_form.validate_on_submit():
        data = movie_form.data
        file_url = secure_filename(movie_form.url.data.filename)
        file_logo = secure_filename(movie_form.logo.data.filename)

        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 6)

        url_name = generate_unique_name(file_url)
        logo_name = generate_unique_name(file_logo)
        movie_form.url.data.save(app.config['UP_DIR'] + url_name)
        movie_form.logo.data.save(app.config['UP_DIR'] + logo_name)

        movie_obj = Movie(
            title=data['title'],
            url=url_name,
            info=data['info'],
            logo=logo_name,
            star=int(data['star']),
            playnum=0,
            commentnum=0,
            tag_id=int(data['tag_id']),
            area=data['area'],
            release_time=data['release_time'],
            length=data['length']
        )
        db.session.add(movie_obj)
        db.session.commit()
        flash('电影添加成功', 'success')
        return redirect(url_for('admin.movie_list', page=1))
    return render_template('admin/movie_add.html', movie_form=movie_form)


@admin.route('/movie/del/<int:id>', methods=["GET", "POST"])
@admin_login_req
def movie_del(id=1):
    movie_obj = Movie.query.get_or_404(int(id))
    db.session.delete(movie_obj)
    db.session.commit()
    flash('电影删除成功!', 'success')
    return redirect(url_for('admin.movie_list', page=1))


@admin.route('/movie/edit/<int:id>', methods=["GET", "POST"])
@admin_login_req
def movie_edit(id=1):
    movie_form = MovieForm()
    movie_form.url.validators = []
    movie_form.logo.validators = []
    movie_obj = Movie.query.get_or_404(int(id))
    if request.method == 'GET':
        movie_form.info.data = movie_obj.info
        movie_form.tag_id.data = movie_obj.tag_id
        movie_form.star.data = movie_obj.star

    if movie_form.validate_on_submit():
        data = movie_form.data
        movie_count = Movie.query.filter_by(title=data['title']).count()
        if movie_count == 1 and movie_obj.title != data['title']:
            flash('该电影已存在!', 'error')
            return redirect(url_for('admin.movie_edit', id=id))

        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 6)

        if movie_form.url.data.filename != '':
            file_url = secure_filename(movie_form.url.data.filename)
            movie_obj.url = generate_unique_name(file_url)
            movie_form.url.data.save(app.config['UP_DIR'] + movie_obj.url)

        if movie_form.logo.data.filename != '':
            file_logo = secure_filename(movie_form.logo.data.filename)
            movie_obj.logo = generate_unique_name(file_logo)
            movie_form.logo.data.save(app.config['UP_DIR'] + movie_obj.logo)

        movie_obj.star = data['star']
        movie_obj.tag_id = data['tag_id']
        movie_obj.info = data['info']
        movie_obj.title = data['title']
        movie_obj.area = data['area']
        movie_obj.length = data['length']
        movie_obj.release_time = data['release_time']

        db.session.add(movie_obj)
        db.session.commit()
        flash('电影修改成功!', 'success')
        return redirect(url_for('admin.movie_add', id=movie_obj.id))
    return render_template("admin/movie_edit.html", movie_form=movie_form, movie_obj=movie_obj)


@admin.route('/movie/list/<int:page>')
@admin_login_req
def movie_list(page=1):
    if page <= 0:
        page = 1
    page_data = Movie.query.join(Tag).filter(Tag.id == Movie.tag_id).order_by(Movie.addtime.desc()).paginate(page=page,
                                                                                                             per_page=10)
    return render_template('admin/movie_list.html', page_data=page_data)


@admin.route('/preview/add/',methods=['GET','POST'])
@admin_login_req
def preview_add():
    preview_form = PreviewForm()
    if preview_form.validate_on_submit():
        data = preview_form.data
        file_logo = secure_filename(preview_form.logo.data.filename)

        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'],6)

        logo = generate_unique_name(file_logo)
        preview_form.logo.data.save(app.config['UP_DIR']+logo)
        preview_obj = Preview(
            title=data['title'],
            logo=logo
        )
        db.session.add(preview_obj)
        db.session.commit()
        flash('预告片添加成功！','success')
        return redirect(url_for('admin.preview_list',page=1))
    return render_template('admin/preview_add.html',preview_form=preview_form)


@admin.route('/preview/list/<int:page>')
@admin_login_req
def preview_list(page=1):
    if page <= 0:
        page = 1
    page_data = Preview.query.order_by(Preview.addtime.desc()).paginate(page=page,per_page=10)
    return render_template('admin/preview_list.html',page_data=page_data)


@admin.route('/preview/del/<int:id>')
@admin_login_req
def preview_del(id=None):
    preview_obj = Preview.query.get_or_404(int(id))
    db.session.delete(preview_obj)
    db.session.commit()
    flash('预告删除成功！','success')
    return redirect(url_for('admin.preview_list',page=1))


@admin.route('/preview/edit/<int:id>',methods=['GET','POST'])
@admin_login_req
def preview_edit(id=None):
    preview_form = PreviewForm()
    preview_obj = Preview.query.get_or_404(int(id))
    if request.method=="GET":
        preview_form.title.data = preview_obj.title

    if preview_form.validate_on_submit():
        data=preview_form.data
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 6)

        if preview_form.logo.data.filename != '':
            file_logo = secure_filename(preview_form.logo.data.filename)
            preview_obj.logo = generate_unique_name(file_logo)
            preview_form.logo.data.save(app.config['UP_DIR'] + preview_obj.logo)

        preview_obj.title = data['title']
        db.session.add(preview_obj)
        db.session.commit()

        flash('预告修改成功!', 'success')
        return redirect(url_for('admin.preview_list',page=1))
    return render_template('admin/preview_edit.html',preview_form=preview_form,preview_obj=preview_obj)


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
