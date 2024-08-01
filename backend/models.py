from .extensions import db, bcrypt
from flask_login import UserMixin

favorites_authors = db.Table('favorites_authors',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('authors.id', ondelete='CASCADE'), primary_key=True)
)

favorites_songs = db.Table('favorites_songs',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    db.Column('song_id', db.Integer, db.ForeignKey('songs.id', ondelete='CASCADE'), primary_key=True)
)


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)
    about = db.Column(db.String, nullable=True)
    songs = db.relationship('Song', backref='author', lazy=True)


class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    lyrics = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='draft')

    user_settings = db.relationship('UserSongSettings', back_populates='song', lazy=True, cascade='all, delete-orphan')
    created_by = db.relationship('User', back_populates='created_songs')


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    favorite_authors = db.relationship('Author', secondary=favorites_authors, lazy='subquery',
                                       backref=db.backref('favorited_by', lazy=True))
    favorite_songs = db.relationship('Song', secondary=favorites_songs, lazy='subquery',
                                     backref=db.backref('favorited_by', lazy=True))
    song_settings = db.relationship('UserSongSettings', back_populates='user', lazy=True, cascade='all, delete-orphan')
    created_songs = db.relationship('Song', back_populates='created_by', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class UserSongSettings(db.Model):
    __tablename__ = 'user_song_settings'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id', ondelete='CASCADE'), primary_key=True)
    transposition = db.Column(db.Integer, nullable=False, default=0)
    capo_position = db.Column(db.Integer, nullable=False, default=0)
    user = db.relationship('User', back_populates='song_settings')
    song = db.relationship('Song', back_populates='user_settings')
