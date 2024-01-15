from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .constants import DICT_SYMBOLS


def get_unique_short_id():
    len_dict = len(DICT_SYMBOLS)
    return ''.join([DICT_SYMBOLS[randrange(len_dict)] for _ in range(6)])


@app.route('/', methods=['GET', 'POST'])
def urlmapform():
    form = URLMapForm()
    if form.validate_on_submit():
        original = form.original_link.data
        short = form.custom_id.data.replace(" ","")
        if len(short) == 0:
            short = get_unique_short_id()

        if URLMap.query.filter_by(short=short).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template(url_for('urlmapform.html', form=form))
        urlmap = URLMap(
            original=original, 
            short=short
        )
        db.session.add(urlmap)
        db.session.commit()
        flash('Ваша новая ссылка готова:')
        flash(url_for('redirect_view', short_id=short, _external=True), 'url')
    return render_template(url_for('urlmapform.html', form=form))


@app.route('/<string:short>/', methods=['GET', ])
def redirect_view(short):
    urlmapform = URLMap.query.filter_by(short=short).first()
    if urlmapform is None:
        abort(404)
    return redirect(urlmapform.original)
