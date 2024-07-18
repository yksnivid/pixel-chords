from flask import Flask, jsonify, request
from .models import Author, Song
from .extensions import db
import random


def register_routes(app: Flask):
    @app.route('/api/songs/random', methods=['GET'])
    def get_random_song():
        songs = Song.query.all()
        if songs:
            random_song = random.choice(songs)
            return jsonify({
                'author': random_song.author.name,
                'title': random_song.title,
                'lyrics': random_song.lyrics
            })
        return jsonify({'error': 'No songs found'}), 404

    @app.route('/api/songs/<author>/<title>', methods=['GET'])
    def get_song(author, title):
        song = Song.query.join(Author).filter(
            Author.name == author,
            Song.title == title
        ).first()
        if song:
            return jsonify({
                'author': song.author.name,
                'title': song.title,
                'lyrics': song.lyrics
            })
        return jsonify({'error': 'Song not found'}), 404

    @app.route('/api/authors', methods=['GET'])
    def get_authors():
        authors = Author.query.all()
        return jsonify([{
            'id': author.id,
            'author': author.name,
            'numberOfSongs': len(author.songs),
            'image': author.image
        } for author in authors])

    @app.route('/api/author/<author>', methods=['GET'])
    def get_author(author):
        author_data = Author.query.filter_by(name=author).first()
        if author_data:
            return jsonify({
                'author': author_data.name,
                'numberOfSongs': len(author_data.songs),
                'coverImage': author_data.image,
                'about': author_data.about,
                'songs': [{'title': song.title, 'value': song.title} for song in author_data.songs]
            })
        return jsonify({'error': 'Author not found'}), 404

    @app.route('/api/songs/add/<author>/<title>', methods=['POST'])
    def add_song(author, title):
        print(author, title)
        data = request.get_json()
        lyrics = data.get('lyrics')

        if not author or not title or not lyrics:
            return jsonify({'error': 'Missing author, title, or lyrics in request data'}), 400

        # Проверяем, существует ли автор в базе данных
        author = Author.query.filter_by(name=author).first()
        if not author:
            return jsonify({'error': f'Author "{author}" not found'}), 404

        # Создаем новую запись песни в базе данных
        new_song = Song(title=title, lyrics=lyrics, author_id=author.id)
        db.session.add(new_song)
        db.session.commit()

        return jsonify({'message': 'Song added successfully'}), 201
