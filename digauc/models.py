from digauc import db, login_manager
from flask import current_app
import jwt
# from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from datetime import datetime, timedelta, timezone
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bid_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    cost = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lot_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return f"Rate('{self.lot_id}', '{self.cost}', '{self.user_id}')"


class Follower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    following_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Follower('{self.follower}', '{self.following}')"


# ------------------------------------------------------------------------
# Удалить дефолты для имени, телефона и тд
# Когда Елисей напишет фронт
# ------------------------------------------------------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Integer, default=0)
    birthday = db.Column(db.DateTime)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    money = db.Column(db.Float, nullable=False, default=0)
    password = db.Column(db.String(60), nullable=False)
    first_name = db.Column(db.String(30), nullable=False, default='Anon')
    second_name = db.Column(db.String(30), default='Anon')
    followers = db.Column(db.Integer, default=0)
    last_name = db.Column(db.String(30), nullable=False, default='Anon')
    phone_number = db.Column(db.String(15), nullable=False, default='88005553535')
    access_lvl = db.Column(db.Integer, nullable=False, default=0)
    subscribers = db.relationship('Follower', foreign_keys="Follower.following_id", backref='following', lazy=True)
    subscribes = db.relationship('Follower', foreign_keys="Follower.follower_id", backref='follower', lazy=True)
    bids = db.relationship('Bid', foreign_keys="Bid.user_id", backref='payer', lazy=True)
    posts = db.relationship('Post', foreign_keys="Post.owner_id", backref='author', lazy=True)
    buys = db.relationship('Post', foreign_keys="Post.buyer_id", backref='buyer', lazy=True)

    # Я хз как его по человечиски делать, там или старье или выкрутасы. Будущий Никита, удачи
    def get_reset_token(self, expires_sec=1800):
        # s = Serializer(app.config['SECRET_KEY'], expires_sec)
        # return s.dumps({'user_id': self.user_id})
        payload = {'user_id': self.id, 'exp': datetime.now(timezone.utc) + timedelta(seconds=expires_sec)}
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# foreign_keys="post.owner_id"


# 0-not created, 1-created,2-started,3-archived
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    date_end = db.Column(db.DateTime, nullable=False, default=(datetime.utcnow() + timedelta(hours=24)))
    status = db.Column(db.Integer, nullable=False, default=0)
    content = db.Column(db.Text, nullable=False)
    start_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False, default=0)
    bids = db.relationship('Bid', foreign_keys="Bid.lot_id", backref='lot', lazy=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_file = db.Column(db.String(20))

    # selling_FILE = db.Column(db.String(100))

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.content}')"


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20))

    def __repr__(self):
        return f"News('{self.title}', '{self.date_posted}', '{self.content}')"
