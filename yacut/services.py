import urllib

import aiohttp
from flask import current_app, abort
from werkzeug.utils import secure_filename

from .constants import API_HOST, API_VERSION

REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'


async def upload_file(file):
    disk_token = current_app.config['DISK_TOKEN']
    auth_headers = {'Authorization': f'OAuth {disk_token}'}
    filename = secure_filename(file.filename)
    payload = {
        'path': f'app:/{filename}',
        'overwrite': 'True'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(REQUEST_UPLOAD_URL, headers=auth_headers,
                               params=payload) as get_response:
            response_data = await get_response.json()
            upload_url = response_data['href']

            file_data = file.read()
            async with session.put(upload_url, data=file_data) as put_response:
                location = put_response.headers.get('Location')

    if location:
        location = urllib.parse.unquote(location)
        location = location.replace('/disk', '')
        return location
    abort(500)


async def get_download_link(file_path):
    disk_token = current_app.config['DISK_TOKEN']
    auth_headers = {'Authorization': f'OAuth {disk_token}'}
    params = {'path': file_path}

    async with aiohttp.ClientSession() as session:
        async with session.get(DOWNLOAD_LINK_URL, headers=auth_headers,
                               params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data['href']

            return None