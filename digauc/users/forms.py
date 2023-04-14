from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from digauc.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=7, max=15)])

    email = StringField('Email', validators=[DataRequired(), Email()])
    # phone = StringField('Phone number',
    #                     validators=[DataRequired(), Length(min=7, max=15), Regexp(regex='^[+-]?[0-9]$')])
    # first_name = StringField('First name', validators=[DataRequired(), Length(min=1, max=30)])
    # last_name = StringField('Last name', validators=[DataRequired(), Length(min=1, max=30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    # Вопросики на счет EqualTo('password')
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        print('check valid username: ' + username.data)
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Данный никнейм уже занят! Пожалуйста выберите другой')

    def validate_email(self, email):
        print('check valid email: ' + email.data)
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Почта уже зарегестрирована!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    # username = StringField('Username',
    #                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=7, max=15)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    picture = FileField('Изменить аватар', validators=[FileAllowed(['jpg', 'png'])])
    # phone = StringField('Phone number',
    #                     validators=[DataRequired(), Length(min=7, max=15), Regexp(regex='^[+-]?[0-9]$')])
    # first_name = StringField('First name', validators=[DataRequired(), Length(min=1, max=30)])
    # last_name = StringField('Last name', validators=[DataRequired(), Length(min=1, max=30)])

    submit = SubmitField('Обновить профиль')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Имя пользователя уже занято")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Почта уже зарегистрирована")


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    # Вопросики на счет EqualTo('password')
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Изменить пароль')