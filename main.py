from datetime import datetime, timedelta

from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '71d2938611327db4e1369b4fbd2e57cc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


# app.app_context().push()
# app.config['SQLALCHEMY DATABASE_URI'] ='sqlite:///blog.db'


# def set_image(gender):
#     if gender == 0:
#         return 'defaultMan.jpg'
#     if gender == 1:
#         return 'defaultMan.jpg'
#     else:
#         return 'defaultWoman.jpg'


# 0-no stated, 1-male, 2-female
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Integer, default=0)
    birthday = db.Column(db.DateTime)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    money = db.Column(db.Float, nullable=False, default=0)
    password = db.Column(db.String(60), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    second_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    access_lvl = db.Column(db.Integer, nullable=False, default=0)
    posts = db.relationship('Post', foreign_keys="Post.owner_id", backref='author', lazy=True)
    buys = db.relationship('Post', foreign_keys="Post.buyer_id", backref='buyer', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# foreign_keys="post.owner_id"
#


# 0-not created, 1-created,2-started,3-archived
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    date_end = db.Column(db.DateTime, nullable=False, default=(datetime.utcnow()))
    status = db.Column(db.Integer, nullable=False, default=0)
    content = db.Column(db.Text, nullable=False)
    start_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False, default=start_price)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_file = db.Column(db.String(20))

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.content}')"


# users = [
#     {
#         'name': 'Brigada',
#         'id': 1220
#     },
#     {
#         'name': 'Shishki',
#         'id': 420
#     }
# ]


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/user/<string:name>/<user_id>')
def user(name, user_id):
    return "About user " + name + " - " + str(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created fo {form.last_name.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.email.data == 'admin@log.ru' and form.password.data == 'password':
        flash('You logged in !', 'success')
        print("succ")
        return redirect(url_for('index'))
    else:
        flash('Login is unsuccessful', 'danger')
        print("bad")
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__":
    app.run(debug=True)
