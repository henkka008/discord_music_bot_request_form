from datetime import datetime
from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.string(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class DiscordChannel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

class MusicRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    date_from = db.Column(db.Date, nullable=False)
    date_to = db.Column(db.Date, nullable=False)
    time_from = db.Column(db.Time, nullable=False)
    time_to = db.Column(db.Time, nullable=False)

    channel_id = db.Column(db.Integer, db.ForeignKey("discord_channel.id"), nullable=False)
    channel = db.relationship("DiscordChannel")

    music_type = db.Column(db.String(200), nullable=False)

    status = db.Column(db.String(20), nullable=False, default="PENDING")

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    