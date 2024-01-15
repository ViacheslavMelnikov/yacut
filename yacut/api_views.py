import re
from flask import jsonify, request
from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id
from .constants import MAX_LEN_SHORT


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    
    if not data.get('custom_id'):
        data['custom_id'] = get_unique_short_id()
    else:
        if re.match(
            r'^[a-zA-Z0-9]+$',
            data['custom_id']) or len(data['custom_id']) > MAX_LEN_SHORT:
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    
    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.')

    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': urlmap.original}), 200
