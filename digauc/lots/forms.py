from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from datetime import datetime, timedelta
from wtforms import StringField, SubmitField, TextAreaField, FloatField, DateField
from wtforms.validators import DataRequired, ValidationError


def validate_date_start(date_start):
    # date_now = datetime.utcnow()
    # date_now = date_now.replace(hour=0, minute=0, second=0, microsecond=0)
    if date_start.data < datetime.utcnow().date():
        raise ValidationError("Время начала указано неверно")


class PostForm(FlaskForm):
    title = StringField('Наименование', validators=[DataRequired()])
    content = TextAreaField('Расскажите о лоте', validators=[DataRequired()])
    start_price = FloatField('Начальная цена', validators=[DataRequired()])
    picture = FileField('Фото', validators=[FileAllowed(['jpg', 'png'])])
    #    user = User.query.filter_by(email=current_user.email).first()
    #   user_id = user.id
    date_start = DateField('Если пропустить, то начнется сейчас', default=datetime.utcnow())
    date_end = DateField('Если пропустить, то зак через 24 часа', default=datetime.utcnow() + timedelta(hours=24))

    submit = SubmitField('Выставить')

    def validate_date_end(self, date_end):
        date_start = self.date_start.data
        print(date_start)
        print(date_end.data)
        if date_end.data < date_start:
            raise ValidationError("Время окончания указано неверно")
