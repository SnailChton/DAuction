import os

import secrets  # Че она красаная, блинб
from flask import url_for, current_app
from PIL import Image

from digauc import lots


def save_lot_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/lot_pics', picture_fn)

    # output_size = (125, 125)
    i = Image.open(form_picture)
    # i.thumbnail()#(output_size)
    i.save(picture_path)

    return picture_fn