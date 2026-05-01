from flask_wtf import FlaskForm
from wtforms import URLField, StringField, SubmitField
from wtforms.validators import (DataRequired, Length, ValidationError,
                                Regexp, Optional)
from flask_wtf.file import MultipleFileField, FileRequired

from .models import URLMap


class URLForm(FlaskForm):
    original_link = URLField(
        'Добавьте ссылку',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки (Опционально)',
        validators=[
            Length(max=16, message='Максимум 16 символов'),
            Optional(),
            Regexp(
                r'^[A-Za-z0-9]+$',
                message='Допустимы только латинские буквы и цифры'
            )
        ]
    )
    submit = SubmitField('Добавить')

    def validate_custom_id(self, field):
        if field.data:
            if field.data == 'files':
                raise ValidationError(
                    'Предложенный вариант короткой ссылки уже существует.')

            existing_id = URLMap.query.filter_by(short=field.data).first()
            if existing_id:
                raise ValidationError(
                    'Предложенный вариант короткой ссылки уже существует.')


class FileForm(FlaskForm):
    files = MultipleFileField(
        'Загрузка файлов',
        validators=[FileRequired(
            message='Пожалуйста, выберите хотя бы один файл')]
    )
    submit = SubmitField('Добавить')
