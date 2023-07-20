from datetime import datetime

from settings import MAX_USER_URL_LENGTH

from . import db
from .utils import get_short_url


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, unique=True, nullable=False)
    short = db.Column(
        db.String(MAX_USER_URL_LENGTH), unique=True, nullable=False, index=True
    )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        if not kwargs.get('short', None):
            kwargs['short'] = get_short_url(db.session, URLMap)
        super().__init__(*args, **kwargs)
