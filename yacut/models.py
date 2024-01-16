from datetime import datetime
from flask import url_for
from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(), unique=False, nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        # Добавляем в модель метод-сериализатор
        short_link = url_for('urlmap_view', _external=True) + self.short
        return dict(
            url=self.original,
            short_link=short_link
        )

    def from_dict(self, data):
        # Добавляем в модель метод-десериализатор
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])