from flask import Flask, jsonify, request
from flask_login import login_required, current_user
from .models import Author, Song, UserSongSettings
from .extensions import db
import random
from fuzzywuzzy import process
from sqlalchemy import or_


def register_routes(app: Flask):
    @app.route('/api/songs/random', methods=['GET'])
    def get_random_song():
        total_count = Song.query.count()
        random_index = random.randint(1, total_count)
        song = Song.query.offset(random_index - 1).limit(1).first()

        if song:

            return jsonify({
                'id': song.id,
                'author': {
                    'id': song.author.id
                }
            })

        return jsonify({'error': 'No songs found'}), 404

    @app.route('/api/songs/<song_id>', methods=['GET'])
    def get_song(song_id):
        song = Song.query.get(song_id)

        if song:

            is_favorite = False
            transpose_semitones = 0
            capo_position = 0

            if current_user.is_authenticated:

                user_song_settings = UserSongSettings.query.filter_by(user_id=current_user.id, song_id=song_id).first()
                if user_song_settings:
                    transpose_semitones = user_song_settings.transposition
                    capo_position = user_song_settings.capo_position

                is_favorite = song.id in {song.id for song in current_user.favorite_songs}

            return jsonify({
                # common fields
                'id': song.id,
                'title': song.title,
                'lyrics': song.lyrics,
                'author': {
                    'id': song.author.id,
                    'name': song.author.name,
                    'image': song.author.image
                },
                # user specified settings
                'isFavorite': is_favorite,
                'transposeSemitones': transpose_semitones,
                'capoPosition': capo_position
            })

        return jsonify({'error': 'Song not found'}), 404

    @app.route('/api/songs/recent', methods=['GET'])
    def get_recent_songs():

        if not current_user.is_authenticated:
            songs = Song.query.filter_by(status='published')
        elif current_user.role == 'admin':
            songs = Song.query
        else:
            songs = Song.query.filter(
                or_(
                    Song.status == 'published',
                    Song.created_by_id == current_user.id
                )
            )

        songs = songs.order_by(Song.id.desc()).limit(10).all()

        if songs:

            if current_user.is_authenticated:
                favorite_songs_ids = {song.id for song in current_user.favorite_songs}
            else:
                favorite_songs_ids = set()

            return jsonify([{
                # common fields
                'id': song.id,
                'title': song.title,
                'author': {
                    'id': song.author.id,
                    'name': song.author.name,
                    'image': song.author.image
                },
                # user specified settings
                'isFavorite': song.id in favorite_songs_ids

            } for song in songs])

        return jsonify({'error': 'Song not found'}), 404

    @app.route('/api/users/<int:user_id>/favorites', methods=['GET'])
    @login_required
    def get_favorites(user_id):

        if user_id != current_user.id:
            return jsonify({'error': 'Unauthorized to getting favorites'}), 401

        data = {
            'songs': [{
                'id': song.id,
                'title': song.title,
                'author': {
                    'id': song.author.id,
                    'name': song.author.name,
                    'image': song.author.image
                },
                'isFavorite': True
            } for song in current_user.favorite_songs],

            'authors': [{
                'id': author.id,
                'name': author.name,
                'numberOfSongs': len(author.songs),
                'image': author.image,
                'isFavorite': True

            } for author in current_user.favorite_authors]
        }

        return jsonify(data), 200

    @app.route('/api/authors', methods=['GET'])
    def get_authors():
        authors = Author.query.order_by(Author.name).all()

        if authors:

            if current_user.is_authenticated:
                favorite_authors_ids = {author.id for author in current_user.favorite_authors}
            else:
                favorite_authors_ids = set()

            return jsonify([{
                # common fields
                'id': author.id,
                'name': author.name,
                'numberOfSongs': len(author.songs),
                'image': author.image,
                # user specific fields
                'isFavorite': author.id in favorite_authors_ids
            } for author in authors])

        return jsonify({'error': 'Authors not found'}), 404

    @app.route('/api/authors/<int:author_id>', methods=['GET'])
    def get_author(author_id):

        author = Author.query.get(author_id)

        if author:

            if current_user.is_authenticated:
                favorite_authors_ids = {author.id for author in current_user.favorite_authors}
                favorite_songs_ids = {song.id for song in current_user.favorite_songs}
            else:
                favorite_authors_ids = set()
                favorite_songs_ids = set()

            if not current_user.is_authenticated:
                songs = [song for song in author.songs if song.status == 'published']
            elif current_user.role != 'admin':
                songs = [song for song in author.songs if song.status == 'published' or song.created_by_id == current_user.id]
            elif current_user.role == 'admin':
                songs = author.songs

            return jsonify({
                # common fields
                'id': author.id,
                'name': author.name,
                'numberOfSongs': len(author.songs),
                'image': author.image,
                'about': author.about,
                # user specific field
                'isFavorite': author.id in favorite_authors_ids,
                # common fields
                'songs': [{
                    'id': song.id,
                    'title': song.title,
                    'status': song.status,
                    'created_by_id': song.created_by_id,
                    # user specific field
                    'isFavorite': song.id in favorite_songs_ids
                } for song in songs]
            })
        return jsonify({'error': 'Author not found'}), 404

    @app.route('/api/songs', methods=['POST'])
    @login_required
    def create_song():

        data = request.get_json()

        author_id = data.get('author_id')
        title = data.get('title')
        lyrics = data.get('lyrics')

        if not author_id or not title or not lyrics:
            return jsonify({'error': 'Missing author, title, or lyrics in request data'}), 400

        author = Author.query.get(author_id)
        if not author:
            return jsonify({'error': f'Author with id={author_id} not found'}), 404

        new_song = Song(
            title=title,
            lyrics=lyrics,
            author_id=author.id,
            created_by_id=current_user.id,
            status='published' if current_user.role == 'admin' else 'draft'
        )
        db.session.add(new_song)
        db.session.commit()

        return jsonify({'message': 'Song added successfully', 'id': new_song.id}), 201

    @app.route('/api/songs/<int:song_id>', methods=['PUT'])
    @login_required
    def update_song(song_id):

        if current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized to update song'}), 401

        data = request.get_json()

        title = data.get('title')
        lyrics = data.get('lyrics')

        if not title or not lyrics:
            return jsonify({'error': 'Missing title or lyrics in request data'}), 400

        song = Song.query.get(song_id)
        if not song:
            return jsonify({'error': f'Song with id={song_id} not found'}), 404

        song.title = title
        song.lyrics = lyrics
        db.session.commit()

        return jsonify({'message': 'Song updated successfully'}), 200

    @app.route('/api/songs/<int:song_id>', methods=['DELETE'])
    @login_required
    def delete_song(song_id):

        if current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized to delete song'}), 401

        song = Song.query.get(song_id)

        if not song:
            return jsonify({'error': f'Song with id={song_id} not found'}), 404

        db.session.delete(song)
        db.session.commit()

        return jsonify({'message': 'Song deleted successfully'}), 200

    @app.route('/api/authors', methods=['POST'])
    @login_required
    def create_author():

        if current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized to create author'}), 401

        data = request.get_json()

        name = data.get('name')
        about = data.get('about')
        image = data.get('image')

        if not name or not about:
            return jsonify({'error': 'Missing name or about in request data'}), 400

        new_author = Author(name=name, about=about, image=image)
        db.session.add(new_author)
        db.session.commit()

        return jsonify({'message': 'Author added successfully', 'id': new_author.id}), 201

    @app.route('/api/authors/<int:author_id>', methods=['PUT'])
    @login_required
    def update_author(author_id):

        if current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized to update author'}), 401

        data = request.get_json()

        name = data.get('name')
        about = data.get('about')
        # image = data.get('image')

        if not name or not about:
            return jsonify({'error': 'Missing name or about in request data'}), 400

        author = Author.query.get(author_id)

        if not author:
            return jsonify({'error': f'Author with id={author_id} not found'}), 404

        author.name = name
        author.about = about
        # author.image = image
        db.session.commit()

        return jsonify({'message': 'Author updated successfully'}), 200

    @app.route('/api/authors/<int:author_id>', methods=['DELETE'])
    @login_required
    def delete_author(author_id):

        if current_user.role!= 'admin':
            return jsonify({'error': 'Unauthorized to delete author'}), 401

        author = Author.query.get(author_id)

        if not author:
            return jsonify({'error': f'Author with id={author_id} not found'}), 404

        db.session.delete(author)
        db.session.commit()

        return jsonify({'message': 'Author deleted successfully'}), 200

    @app.route('/api/users/<int:user_id>/favorites', methods=['POST', 'DELETE'])
    @login_required
    def manage_favorite_item(user_id):

        if current_user.id != user_id:
            return jsonify({'error': 'Unauthorized to manage favorites'}), 401

        data = request.get_json()
        item_id = data.get('item_id')
        item_type = data.get('item_type')

        if item_type == 'author':
            item = Author.query.get(item_id)
            favorite_list = current_user.favorite_authors
        elif item_type == 'song':
            item = Song.query.get(item_id)
            favorite_list = current_user.favorite_songs
        else:
            return jsonify({'error': 'Invalid item type'}), 400

        if not item:
            return jsonify({'error': f'{item_type.capitalize()} not found'}), 404

        if request.method == 'POST':
            if item in favorite_list:
                return jsonify({'error': f'{item_type.capitalize()} already in favorites'}), 422
            else:
                favorite_list.append(item)
                db.session.commit()
                return jsonify({'message': f'{item_type.capitalize()} added to favorites'}), 200

        if request.method == 'DELETE':
            if item not in favorite_list:
                return jsonify({'error': f'{item_type.capitalize()} already not in favorites'}), 422
            else:
                favorite_list.remove(item)
                db.session.commit()
                return jsonify({'message': f'{item_type.capitalize()} removed from favorites'}), 200

    @app.route('/api/users/<int:user_id>/songs/<int:song_id>/settings', methods=['PUT'])
    @login_required
    def update_song_settings(user_id, song_id):

        if current_user.id != user_id:
            return jsonify({'error': 'Unauthorized to manage song settings'}), 401

        user_song_settings = UserSongSettings.query.filter_by(user_id=user_id, song_id=song_id).first()

        data = request.get_json()
        capo_position = data.get('capoPosition')
        transpose_semitones = data.get('transposeSemitones')

        if not isinstance(capo_position, int) or not 0 <= capo_position <= 12:
            return jsonify({'error': 'Invalid capo position'}), 400

        if not isinstance(transpose_semitones, int) or not -12 <= transpose_semitones <= 12:
            return jsonify({'error': 'Invalid transpose semitones'}), 400

        if not user_song_settings:
            user_song_settings = UserSongSettings(user_id=user_id, song_id=song_id)
            db.session.add(user_song_settings)

        user_song_settings.transposition = transpose_semitones
        user_song_settings.capo_position = capo_position

        db.session.commit()

        return jsonify({'message': 'Successfully updated'}), 200

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
            if match[1] >= 50:  # Порог подобия 50%
                matching_songs.append(song)

        if matching_songs:
            response['songs'] = [{
                'id': song.id,
                'title': song.title,
                'author': {
                    'id': song.author.id,
                    'name': song.author.name
                }
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
