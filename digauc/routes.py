from flask import Flask, render_template, url_for, flash, redirect
from digauc import app
from digauc.forms import RegistrationForm, LoginForm
from digauc.models import User, Post, News, Bid, Follower


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

