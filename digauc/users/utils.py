import os

import PIL
import secrets  # Че она красаная, блинб
from PIL import Image
from flask import url_for, current_app
from digauc import lots, mail
from flask_mail import Message

from flask_login import current_user


def save_user_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    if current_user.image_file != 'default.jpg':
        os.remove(current_app.root_path + '\static\profile_pics\\' + current_user.image_file)

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


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@digauc.com', recipients=[user.email])
    msg.body = f'''To Reset your password visit forward link:
{url_for('reset_token', token=token, _external=True)}

If you did not request  then simply ignore that message
'''
    mail.send(msg)
