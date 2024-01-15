from random import randrange

from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .constants import DICT_SYMBOLS
from .error_handlers import InvalidAPIUsage


def get_unique_short_id():
    len_dict = len(DICT_SYMBOLS)
    return ''.join([DICT_SYMBOLS[randrange(len_dict)] for _ in range(6)])


@app.route('/', methods=['GET', 'POST'])
def urlmap_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original = form.original_link.data
        short = form.custom_id.data.replace(" ","")
        if len(short) == 0:
            short = get_unique_short_id()

        if URLMap.query.filter_by(short=short).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        urlmap = URLMap(
            original=original, 
            short=short
        )
        db.session.add(urlmap)
        db.session.commit()
        flash('Ваша новая ссылка готова:', 'shorturl_message1')
        create_short_url = url_for('redirect_view', short=short, _external=True)
        flash(create_short_url, 'shorturl_message2')
    return render_template('index.html', form=form)


@app.route('/<string:short>/', methods=['GET', ])
def redirect_view(short):
    urlmap = URLMap.query.filter_by(short=short).first()
    if urlmap is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return redirect(urlmap.original)
