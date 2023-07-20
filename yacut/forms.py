from flask_wtf import FlaskForm
from settings import MAX_USER_URL_LENGTH
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class YacutForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=(DataRequired(message='Обязательное поле'),),
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=(Length(1, MAX_USER_URL_LENGTH), Optional()),
    )
    submit = SubmitField('Добавить')
