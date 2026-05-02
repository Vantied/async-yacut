import string
import secrets

from .models import URLMap
from .constants import GENERATED_ID_LENGTH


def get_unique_short_id():
    """Генерирует уникальную случайную строку."""
    characters = string.ascii_letters + string.digits
    while True:
        short_url = ''.join(secrets.choice(characters)
                            for _ in range(GENERATED_ID_LENGTH))
        if not URLMap.query.filter_by(short=short_url).first():
            return short_url