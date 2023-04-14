from flask import Blueprint, render_template
from flask_login import login_required

from sqlalchemy import desc

from digauc.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def index():
    # С пагинацией
    # page = request.args.get('page', 1, type=int)
    # lots = Post.query.order_by(desc(Post.date_posted)).paginate(page=page, per_page=4)

    # Без пагинации
    posts = Post.query.order_by(desc(Post.date_posted)).all()

    # Просто проверочка, надобы вырезать, но я люблю коллекционировать мусор
    # post = Post.query.filter_by(image_file='190d4023d6e70ac3.jpg').first()
    # print(post.owner_id)
    # print(post.image_file)
    # image_file = url_for('static', filename='lot_pics/' + lots.image_file)
    return render_template("index.html", posts=posts)


@main.route('/about')
def about():
    return render_template("about.html")


# @app.route('/account')
# def user(name, user_id):
#     return "About user " + name + " - " + str(user_id)
