#from flask import Flask, render_template, url_for, flash, redirect
#from flask_sqlalchemy import SQLAlchemy

#from digauc.forms import RegistrationForm, LoginForm

# app = Flask(__name__)
# app.config['SECRET_KEY'] = '71d2938611327db4e1369b4fbd2e57cc'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db = SQLAlchemy(app)


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
from digauc import app

if __name__ == "__main__":
    app.run(debug=True)
