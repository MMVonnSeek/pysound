from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Tabela de associação: muitos-para-muitos entre Playlist e Song
playlist_songs = db.Table('playlist_songs',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id')),
    db.Column('song_id',     db.Integer, db.ForeignKey('song.id'))
)

class User(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(80), unique=True, nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    songs     = db.relationship('Song',     backref='owner', lazy=True)
    playlists = db.relationship('Playlist', backref='owner', lazy=True)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}

class Song(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(200), nullable=False)
    artist     = db.Column(db.String(200), nullable=False)
    album      = db.Column(db.String(200))
    duration   = db.Column(db.Integer)          # duração em segundos
    genre      = db.Column(db.String(100))
    url        = db.Column(db.String(500))       # URL do arquivo/stream
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id, "title": self.title, "artist": self.artist,
            "album": self.album, "duration": self.duration,
            "genre": self.genre, "url": self.url,
            "added_by": self.owner.username
        }

class Playlist(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    songs       = db.relationship('Song', secondary=playlist_songs, lazy='subquery',
                                  backref=db.backref('playlists', lazy=True))

    def to_dict(self):
        return {
            "id": self.id, "name": self.name,
            "description": self.description,
            "owner": self.owner.username,
            "songs": [s.to_dict() for s in self.songs],
            "total_songs": len(self.songs)
        }