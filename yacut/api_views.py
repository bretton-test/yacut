from flask import jsonify, request, url_for
from sqlalchemy.exc import IntegrityError

from . import app, db
from .error_handlers import InvalidAPIUsage, ShortUrlGenerationError
from .models import URLMap
from .utils import get_or_create, validate_short_url, validate_url


@app.route('/api/id/', methods=['POST'])
def add_url_map():
    data = request.get_json(silent=True)
    result = validate_url(data)
    if result:
        raise InvalidAPIUsage(result)
    url, short_url = data.get('url'), data.get('custom_id', None)
    if short_url:
        result = validate_short_url(db.session, URLMap, short_url, True)
        if result:
            raise InvalidAPIUsage(result)

    try:
        url_map = get_or_create(db.session, URLMap, original=url)
        if short_url:
            url_map.short = short_url
        db.session.commit()
        short_link = url_for('index_view', _external=True) + url_map.short
        return jsonify({'url': url, 'short_link': short_link}), 201
    except (IntegrityError, ShortUrlGenerationError) as error:
        raise InvalidAPIUsage(error, status_code=500)


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_url_for(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200
