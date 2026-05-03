import re
import string
import secrets

from sqlalchemy.sql import func
from yacut import db

from .constants import (MAX_CUSTOM_ID_LENGTH,
                        GENERATED_ID_LENGTH,
                        ATTEMPTS_TO_GENERATE,
                        SHORT_ID_PATTERN,
                        FORBIDDEN_ID
                        )


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String(MAX_CUSTOM_ID_LENGTH), nullable=True)
    timestamp = db.Column(db.DateTime, index=True, server_default=func.now())

    @classmethod
    def get(cls, short_id):
        """Получить объект из БД, если нет вернёт None"""
        return cls.query.filter_by(short=short_id).first()

    @classmethod
    def get_unique_short_id(cls):
        """
        Генерирует уникальную случайную строку, если не смогла вызовит ошибку
        """
        characters = string.ascii_letters + string.digits
        for _ in range(ATTEMPTS_TO_GENERATE):
            short_url = ''.join(secrets.choice(characters)
                                for _ in range(GENERATED_ID_LENGTH))
            if not cls.get(short_url):
                return short_url
        raise ValueError('Произошла ошибка при генерации ссылки')

    def to_dict(self):
        return dict(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp
        )

    def from_dict(self, data):
        self.original = data.get('original')
        self.short = data.get('short')

    def save(self):
        """Проверяет и сохраняет в БД данные"""
        if not self.short:
            self.short = self.get_unique_short_id()

        if (len(self.short) > MAX_CUSTOM_ID_LENGTH or
                not re.match(SHORT_ID_PATTERN, self.short)):
            raise ValueError(
                'Указано недопустимое имя для короткой ссылки')

        if (self.short in FORBIDDEN_ID or
                self.get(self.short)):
            raise ValueError(
                'Предложенный вариант короткой ссылки уже существует.')
        db.session.add(self)
        db.session.commit()
