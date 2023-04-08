import os

import PIL
import secrets
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request, abort
from digauc import app, db, bcrypt
from digauc.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from digauc.models import User, Post, News, Bid, Follower
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import desc


@app.route('/')
@app.route('/home')
def index():
    # С пагинацией
    # page = request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(desc(Post.date_posted)).paginate(page=page, per_page=4)

    # Без пагинации
    posts = Post.query.order_by(desc(Post.date_posted)).all()

    # Просто проверочка
    # post = Post.query.filter_by(image_file='190d4023d6e70ac3.jpg').first()
    # print(post.owner_id)
    # print(post.image_file)
    # image_file = url_for('static', filename='lot_pics/' + posts.image_file)
    return render_template("index.html", posts=posts)


@app.route('/about')
def about():
    return render_template("about.html")


# @app.route('/account')
# def user(name, user_id):
#     return "About user " + name + " - " + str(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Вы успешно зарегистрировались!', 'success')
        print('registr good')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login is unsuccessful, check email and password', 'danger')
            print("login bad")
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_lot_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/lot_pics', picture_fn)

    # output_size = (125, 125)
    i = Image.open(form_picture)
    # i.thumbnail()#(output_size)
    i.save(picture_path)

    return picture_fn


def save_user_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    if current_user.image_file != 'default.jpg':
        os.remove(app.root_path + '\static\profile_pics\\' + current_user.image_file)

    fixed_height = 480
    i_fix = Image.open(form_picture)
    height_percent = (fixed_height / float(i_fix.size[1]))
    width_size = int((float(i_fix.size[0]) * float(height_percent)))
    i_fix = i_fix.resize((width_size, fixed_height), PIL.Image.NEAREST)
    i_fix.save(picture_path)

    # method 2(for optimizing server)
    # output_size = (480, 480)
    # i = Image.open(form_picture)
    # i.thumbnail(output_size)
    # i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_user_picture(form.picture.data)
            current_user.image_file = picture_file
            # print('picture mock_print')

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Нахуя в акк насрал?', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            print('pic exist')
            picture_file = save_lot_picture(form.picture.data)
            print(picture_file)
            post = Post(title=form.title.data, content=form.content.data,
                        date_posted=form.date_start.data, date_end=form.date_end.data,
                        image_file=picture_file,
                        author=current_user, start_price=form.start_price.data)
            print(post.image_file)
        else:
            print('pic doesnt exist')
            post = Post(title=form.title.data, content=form.content.data,
                        date_posted=form.date_start.data, date_end=form.date_end.data,
                        author=current_user, start_price=form.start_price.data)
        db.session.add(post)
        db.session.commit()
        flash('Лот зарегестрирован', 'success')
        return redirect(url_for('index'))
    return render_template('create_post.html', title='New Lot',
                           form=form, legend='New Post')


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


# !----------------Не работает----------------!#
@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    if post.status >= 2:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if form.picture.data:
            print('pic exist')
            picture_file = save_lot_picture(form.picture.data)
            post.image_file = picture_file
        post.date_posted = form.date_start.data
        post.date_end = form.date_end.data
        post.start_price = form.start_price.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.start_price = post.start_price
        form.date_start = post.date_posted
        form.date_end = post.date_end
        if post.image_file:
            picture_fn = post.image_file
            picture_path = os.path.join(app.root_path, 'static/lot_pics', picture_fn)
            i = Image.open(picture_path)
            # output_size = (400, 400)
            # i = Image.open(form_picture)
            form.picture = i
    return render_template('create_post.html', title='Update Lot',
                           form=form, legend='Update Post')


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    if post.status >= 2:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))


@app.route('/user/<string:username>')
def user_posts(username):
    # С пагинацией
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(desc(Post.date_posted))\
        .paginate(page=page, per_page=4)

    return render_template("user_posts.html", posts=posts, user=user)
