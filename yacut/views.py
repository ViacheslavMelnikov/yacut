import re
from http import HTTPStatus
from random import choice

from flask import flash, redirect, render_template, url_for

from . import app, db
from .constants import SYMBOLS, MAX_LEN_SHORT_AUTO
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id():
    return ''.join(choice(SYMBOLS) for _ in range(MAX_LEN_SHORT_AUTO))


@app.route('/', methods=['GET', 'POST'])
def urlmap_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original = form.original_link.data
        short = form.custom_id.data
        if not short or re.match(r'^\s*$', short):
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
        create_short_url = url_for('urlmap_view', _external=True) + short
        flash(create_short_url, 'shorturl_message2')
    return render_template('index.html', form=form)


@app.route('/<string:short_id>', methods=['GET', ])
def redirect_view(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(urlmap.original, code=HTTPStatus.FOUND)
