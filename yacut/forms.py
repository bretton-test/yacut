from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from settings import MAX_USER_URL_LENGTH, SHORT_URL_REGEXP


class YacutForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=(DataRequired(message='Обязательное поле'),),
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=(
            Length(1, MAX_USER_URL_LENGTH),
            Optional(),
            Regexp(
                SHORT_URL_REGEXP,
                message="url must contain only letters numbers",
            ),
        ),
    )
    submit = SubmitField('Добавить')
