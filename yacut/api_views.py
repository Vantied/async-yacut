import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def add_short_id():
    data = request.get_json(silent=True)

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    try:
        url = URLMap(
            original=data.get('url'),
            short=data.get('custom_id')
        )
        url.save()

        return jsonify({
            'url': url.original,
            'short_link': request.host_url + url.short
        }), 201
    except ValueError as e:
        raise InvalidAPIUsage(f'{e}')


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short_url(short_id):
    url = URLMap.get(short_id)
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200