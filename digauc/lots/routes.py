from PIL.Image import Image
import os
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from digauc import db
from digauc.lots.utils import save_lot_picture
from digauc.models import Post
from digauc.lots.forms import PostForm

from flask_login import current_user, login_required

lots = Blueprint('lots', __name__)


@lots.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            print('pic exist')
            picture_file = save_lot_picture(form.picture.data)
            print(picture_file)
            lot = Post(title=form.title.data, content=form.content.data,
                       date_posted=form.date_start.data, date_end=form.date_end.data,
                       image_file=picture_file,
                       author=current_user, start_price=form.start_price.data)
            print(lot.image_file)
        else:
            print('pic doesnt exist')
            lot = Post(title=form.title.data, content=form.content.data,
                       date_posted=form.date_start.data, date_end=form.date_end.data,
                       author=current_user, start_price=form.start_price.data)
        db.session.add(lot)
        db.session.commit()
        flash('Лот зарегестрирован', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_post.html', title='New Lot',
                           form=form, legend='New Post')


@lots.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    lot = Post.query.get_or_404(post_id)
    return render_template('post.html', title=lot.title, post=lot)


# !----------------Не работает----------------!#
@lots.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    lot = Post.query.get_or_404(post_id)
    if lot.author != current_user:
        abort(403)
    if lot.status >= 2:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        lot.title = form.title.data
        lot.content = form.content.data
        if form.picture.data:
            print('pic exist')
            picture_file = save_lot_picture(form.picture.data)
            lot.image_file = picture_file
        lot.date_posted = form.date_start.data
        lot.date_end = form.date_end.data
        lot.start_price = form.start_price.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('lots.post', post_id=lot.id))
    elif request.method == 'GET':
        form.title.data = lot.title
        form.content.data = lot.content
        form.start_price = lot.start_price
        form.date_start = lot.date_posted
        form.date_end = lot.date_end
        if lot.image_file:
            picture_fn = lot.image_file
            picture_path = os.path.join(lots.root_path, 'static/lot_pics', picture_fn)
            i = Image.open(picture_path)
            # output_size = (400, 400)
            # i = Image.open(form_picture)
            form.picture = i
    return render_template('create_post.html', title='Update Lot',
                           form=form, legend='Update Post')


@lots.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    lot = Post.query.get_or_404(post_id)
    if lot.author != current_user:
        abort(403)
    if lot.status >= 2:
        abort(403)
    db.session.delete(lot)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.index'))
