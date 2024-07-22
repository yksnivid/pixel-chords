from flask import Flask, jsonify, request
from flask_login import login_required, current_user
from .models import Author, Song
from .extensions import db
import random
from fuzzywuzzy import process


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

    @app.route('/api/songs/recent', methods=['GET'])
    def get_recent_songs():
        all_songs = Song.query.all()

        if current_user.is_authenticated:
            favorite_song_ids = {song.id for song in current_user.favorite_songs}
        else:
            favorite_song_ids = set()

        if all_songs:
            return jsonify([{
                'id': song.id,
                'author': song.author.name,
                'image': song.author.image,
                'title': song.title,
                'isFavorite': song.id in favorite_song_ids
            } for song in all_songs])
        return jsonify({'error': 'Song not found'}), 404

    @app.route('/api/authors', methods=['GET'])
    def get_authors():
        authors = Author.query.order_by(Author.name).all()
        if current_user.is_authenticated:
            favorite_author_ids = {author.id for author in current_user.favorite_authors}
            response = [{
                'id': author.id,
                'author': author.name,
                'numberOfSongs': len(author.songs),
                'image': author.image,
                'isFavorite': author.id in favorite_author_ids
            } for author in authors]
        else:
            response = [{
                'id': author.id,
                'author': author.name,
                'numberOfSongs': len(author.songs),
                'image': author.image,
                'isFavorite': False  # Неавторизованные пользователи не имеют избранных авторов
            } for author in authors]
        return jsonify(response)

    @app.route('/api/author/<author>', methods=['GET'])
    def get_author(author):

        author_data = Author.query.filter_by(name=author).first()

        if author_data:

            if current_user.is_authenticated:
                favorite_song_ids = {song.id for song in current_user.favorite_songs}
            else:
                favorite_song_ids = set()

            return jsonify({
                'author': author_data.name,
                'numberOfSongs': len(author_data.songs),
                'coverImage': author_data.image,
                'about': author_data.about,
                'songs': [{
                    'id': song.id,
                    'title': song.title,
                    'value': song.title,
                    'isFavorite': song.id in favorite_song_ids
                } for song in author_data.songs]
            })
        return jsonify({'error': 'Author not found'}), 404

    @app.route('/api/songs/add/<author>/<title>', methods=['POST'])
    def add_song(author, title):
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

    @app.route('/api/toggle_favorite_author', methods=['POST'])
    @login_required
    def toggle_favorite_author():
        data = request.get_json()
        author_id = data.get('author_id')

        if not author_id:
            return jsonify({'error': 'Author ID is required'}), 400

        author = Author.query.get(author_id)
        if not author:
            return jsonify({'error': 'Author not found'}), 404

        if author in current_user.favorite_authors:
            current_user.favorite_authors.remove(author)
            is_favorite = False
            message = 'Author removed from favorites'
        else:
            current_user.favorite_authors.append(author)
            is_favorite = True
            message = 'Author added to favorites'

        db.session.commit()

        return jsonify({'message': message, 'author': author.name, 'isFavorite': is_favorite}), 200

    @app.route('/api/toggle_favorite_song', methods=['POST'])
    @login_required
    def toggle_favorite_song():
        data = request.get_json()
        song_id = data.get('song_id')

        if not song_id:
            return jsonify({'error': 'Song ID is required'}), 400

        song = Song.query.get(song_id)
        if not song:
            return jsonify({'error': 'Song not found'}), 404

        if song in current_user.favorite_songs:
            current_user.favorite_songs.remove(song)
            is_favorite = False
            message = 'Song removed from favorites'
        else:
            current_user.favorite_songs.append(song)
            is_favorite = True
            message = 'Song added to favorites'

        db.session.commit()

        return jsonify({'message': message, 'song': song.title, 'isFavorite': is_favorite}), 200

    @app.route('/api/search/<text>', methods=['GET'])
    def search(text):
        response = {
            'authors': [],
            'songs': []
        }

        text_lower = text.lower()

        # Получаем все песни и авторов
        all_songs = Song.query.all()
        all_authors = Author.query.all()

        # Поиск песен по названию и автору с использованием FuzzyWuzzy
        matching_songs = []
        for song in all_songs:
            match = process.extractOne(text_lower, [f'{song.author.name.lower()} {song.title.lower()}'])
            if match[1] >= 50: # Порог подобия 50%
                matching_songs.append(song)

        if matching_songs:
            response['songs'] = [{
                'id': song.id,
                'title': song.title,
                'author': song.author.name,
            } for song in matching_songs]

        # Поиск авторов с использованием FuzzyWuzzy
        matching_authors = []
        for author in all_authors:
            name_match = process.extractOne(text_lower, [author.name.lower()])
            if name_match[1] >= 50:  # Порог подобия 50%
                matching_authors.append(author)

        if matching_authors:
            response['authors'] = [{
                'id': author.id,
                'name': author.name,
                'image': author.image
            } for author in matching_authors]

        return jsonify(response)
