from flask import Flask, render_template, url_for, flash, redirect;
from flask_sqlalchemy import  SQLAlchemy
from datetime import datetime
from forms import RegistrationForm, LoginForm

app = Flask(__name__)


app.config['SECRET_KEY'] = '71d2938611327db4e1369b4fbd2e57cc'


# app.config['SQLALCHEMY DATABASE_URI'] ='sqlite:///blog.db'
# db = SQLAlchemy(app)



# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     last_name = db.Column(db.String(30), nullable=False)
#     second_name = db.Column(db.String(30))
#     first_name = db.Column(db.String(30), nullable=False)
#     phone_number = db.Column(db.String(15), nullable=False)
#     email = db.Column(db.Sring(30))
#     password = db.Column(db.String, nullable=False)
#     access_lvl = db.Column(db.Ineger, nullable=False)
#
#     def __repr__(self):
#         return '<Article %r>' % self.id


users = [
    {
        'name': 'Brigada',
        'id': 1220
    },
    {
        'name': 'Shishki',
        'id': 420
    }
]

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/user/<string:name>/<int:id>')
def user(name,id):
    return "About user "+ name + " - " + str(id);


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created fo {form.last_name.data}!','success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)



if __name__ == "__main__":
    app.run(debug=True)