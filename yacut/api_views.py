import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def add_short_id():
    data = request.get_json(silent=True)

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')
    if not custom_id:
        custom_id = get_unique_short_id()
    else:
        if len(custom_id) > 16 or not re.match(r'^[A-Za-z0-9]+$', custom_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')

        if (custom_id == 'files' or
                URLMap.query.filter_by(short=custom_id).first()):
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.')

    url = URLMap(
        original=data['url'],
        short=custom_id
    )

    db.session.add(url)
    db.session.commit()

    return jsonify({
        'url': url.original,
        'short_link': request.host_url + url.short
    }), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200