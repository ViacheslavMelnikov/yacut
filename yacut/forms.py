from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Optional, Regexp


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Указанный Вами URL-адрес не прошел проверку')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Regexp(
                '^[a-zA-Z0-9]{1,16}$',
                message='Только буквы латинского алфавита и цифры')]
    )
    submit = SubmitField('Создать')