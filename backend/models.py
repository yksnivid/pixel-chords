from .extensions import db, bcrypt
from flask_login import UserMixin

favorites_authors = db.Table('favorites_authors',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('authors.id'), primary_key=True)
)

favorites_songs = db.Table('favorites_songs',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('song_id', db.Integer, db.ForeignKey('songs.id'), primary_key=True)
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
    lyrics = db.Column(db.Text, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)


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

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
