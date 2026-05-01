from sqlalchemy.sql import func
from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String(16), nullable=True)
    timestamp = db.Column(db.DateTime, index=True, server_default=func.now())
