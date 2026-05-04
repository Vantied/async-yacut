from flask_wtf import FlaskForm
from wtforms import URLField, StringField, SubmitField
from wtforms.validators import (DataRequired, Length, ValidationError,
                                Regexp, Optional)
from flask_wtf.file import MultipleFileField, FileRequired

from .models import URLMap
from .constants import MAX_CUSTOM_ID_LENGTH, SHORT_ID_PATTERN


class URLForm(FlaskForm):
    original_link = URLField(
        'Добавьте ссылку',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки (Опционально)',
        validators=[
            Length(max=MAX_CUSTOM_ID_LENGTH,
                   message=f'Максимум {MAX_CUSTOM_ID_LENGTH} символов'),
            Optional(),
            Regexp(
                SHORT_ID_PATTERN,
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

            existing_id = URLMap.get(field.data)
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
