import random
import re

from validators import url as url_validator

from settings import (
    CHARACTERS,
    MAX_TRY_GEN_URL,
    MAX_USER_URL_LENGTH,
    SHORT_URL_LENGTH,
    SHORT_URL_REGEXP,
)
from yacut.error_handlers import ShortUrlGenerationError


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance


def get_short_url(session, model):
    for _ in range(MAX_TRY_GEN_URL):
        s_url = ''.join(random.choices(CHARACTERS, k=SHORT_URL_LENGTH))
        if session.query(model).filter_by(short=s_url).first() is None:
            return s_url
    raise ShortUrlGenerationError('Could not generate short url')


def validate_short_url(session, model, short_url, api=False):
    if len(short_url) > MAX_USER_URL_LENGTH:
        return 'Указано недопустимое имя для короткой ссылки'

    if not re.match(SHORT_URL_REGEXP, short_url):
        return 'Указано недопустимое имя для короткой ссылки'

    if session.query(model).filter_by(short=short_url).first() is not None:
        if api:
            return f'Имя "{short_url}" уже занято.'  # это шутка такая
        return f'Имя {short_url} уже занято!'  # в тестах и так и этак надо


def validate_url(data):
    if data is None:
        return 'Отсутствует тело запроса'
    if 'url' not in data:
        return '\"url\" является обязательным полем!'
    url = data.get('url', None)
    if not url_validator(url):
        return 'invalid url. '
