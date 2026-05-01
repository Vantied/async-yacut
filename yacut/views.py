import secrets
import string

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLForm, FileForm
from .models import URLMap
from .constants import BASE_URL


def get_unique_short_id():
    """Генерирует уникальную случайную строку из 6 символов"""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(6))


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        short_url = form.custom_id.data
        if not short_url:
            while True:
                short_url = get_unique_short_id()
                if not URLMap.query.filter_by(short=short_url).first():
                    break
        url = URLMap(
            original=form.original_link.data,
            short=short_url
        )
        full_url = f'{BASE_URL}/{short_url}'
        db.session.add(url)
        db.session.commit()
        return (render_template('index.html', form=form, short_url=full_url),
                200)
    return render_template('index.html', form=form), 200


@app.route('/<string:short_id>', methods=['GET'])
def redirect_to_url_view(short_id):
    url = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url.original)


@app.route('/upload', methods=['GET', 'POST'])
def upload_view():
    form = FileForm()
    if form.validate_on_submit():
        while True:
            short_url = get_unique_short_id()
            if not URLMap.query.filter_by(short=short_url).first():
                break
        