from flask import abort, flash, redirect, render_template, url_for
from sqlalchemy.exc import IntegrityError

from settings import MAIN_PAGE
from . import app, db
from .error_handlers import ShortUrlGenerationError
from .forms import YacutForm
from .models import URLMap
from .utils import get_or_create, validate_short_url, validate_url


@app.route('/', methods=('GET', 'POST'))
def index_view():
    form = YacutForm()
    if not form.validate_on_submit():
        return render_template(MAIN_PAGE, form=form)

    short_url, url = form.custom_id.data, form.original_link.data
    test_result = validate_url({'url': url}) or ''

    if short_url:
        test_result += validate_short_url(db.session, URLMap, short_url) or ''
    if test_result != '':
        flash(test_result, 'error')
        return render_template(MAIN_PAGE, form=form)

    try:
        url_map = get_or_create(db.session, URLMap, original=url)
        if short_url:
            url_map.short = short_url
        db.session.commit()
        result_url = url_for('index_view', _external=True) + url_map.short
        return render_template(MAIN_PAGE, form=form, result_url=result_url)
    except (IntegrityError, ShortUrlGenerationError):
        abort(500)


@app.route('/<string:s_url>', methods=('GET',))
def redirection(s_url):
    url_map = URLMap.query.filter_by(short=s_url).first_or_404()
    return redirect(url_map.original)
