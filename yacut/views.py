from flask import abort, redirect, render_template, request, flash

from . import app, db
from .forms import URLForm, FileForm
from .models import URLMap
from .services import upload_file, get_download_link
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        try:
            url = URLMap(original=form.original_link.data,
                         short=form.custom_id.data)
            url.save()
            return (render_template(
                'index.html',
                form=form,
                short_url=url.short),
                200
            )
        except ValueError as e:
            flash(str(e), 'danger')
    return render_template('index.html', form=form), 200



@app.route('/<string:short_id>', methods=['GET'])
async def redirect_to_url_view(short_id):
    url = URLMap.query.filter_by(short=short_id).first_or_404()

    if url.original.startswith(('http://', 'https://')):
        return redirect(url.original)

    download_link = await get_download_link(url.original)
    if download_link:
        return redirect(download_link)

    abort(404)


@app.route('/files', methods=['GET', 'POST'])
async def upload_view():
    form = FileForm()
    short_urls = []
    if form.validate_on_submit():
        for file in form.files.data:
            path = await upload_file(file)

            await get_download_link(path)

            short_id = get_unique_short_id()
            url = URLMap(original=path, short=short_id)
            db.session.add(url)

            short_urls.append(f'{file.filename}: {request.host_url}{short_id}')

        db.session.commit()
        return (render_template('upload.html', form=form,
                                short_url=short_urls), 200)
    return render_template('upload.html', form=form), 200
