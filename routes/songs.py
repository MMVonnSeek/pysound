from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Song

songs_bp = Blueprint('songs', __name__)

@songs_bp.route('/', methods=['GET'])
def get_songs():
    # Filtros opcionais via query params: /songs?genre=rock&artist=Beatles
    genre  = request.args.get('genre')
    artist = request.args.get('artist')
    search = request.args.get('q')        # busca geral

    query = Song.query

    if genre:  query = query.filter(Song.genre.ilike(f'%{genre}%'))
    if artist: query = query.filter(Song.artist.ilike(f'%{artist}%'))
    if search:
        query = query.filter(
            db.or_(Song.title.ilike(f'%{search}%'),
                   Song.artist.ilike(f'%{search}%'),
                   Song.album.ilike(f'%{search}%'))
        )

    songs = query.order_by(Song.created_at.desc()).all()
    return jsonify({"songs": [s.to_dict() for s in songs], "total": len(songs)}), 200


@songs_bp.route('/<int:song_id>', methods=['GET'])
def get_song(song_id):
    song = Song.query.get_or_404(song_id)
    return jsonify(song.to_dict()), 200


@songs_bp.route('/', methods=['POST'])
@jwt_required()                          # 🔒 Rota protegida!
def create_song():
    user_id = get_jwt_identity()
    data    = request.get_json()

    if not data or not all(k in data for k in ['title', 'artist']):
        return jsonify({"error": "title e artist são obrigatórios"}), 400

    song = Song(
        title=data['title'], artist=data['artist'],
        album=data.get('album'), duration=data.get('duration'),
        genre=data.get('genre'), url=data.get('url'),
        user_id=int(user_id)
    )
    db.session.add(song)
    db.session.commit()
    return jsonify({"message": "Música adicionada!", "song": song.to_dict()}), 201


@songs_bp.route('/<int:song_id>', methods=['DELETE'])
@jwt_required()
def delete_song(song_id):
    user_id = int(get_jwt_identity())
    song    = Song.query.get_or_404(song_id)

    if song.user_id != user_id:
        return jsonify({"error": "Sem permissão para deletar esta música"}), 403

    db.session.delete(song)
    db.session.commit()
    return jsonify({"message": "Música removida!"}), 200