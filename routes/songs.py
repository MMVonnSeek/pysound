from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identify
from models import db, Song

songs_bp = Blueprint('songs', __name__)

@songs_bp.route('/', methods=['GET'])
def get_songs():
    # Filtros opcionais via query 
    genre = request.args.get('genre')
    artist = request.args.get( 'artist')
    search = request.args.get('q')

    query = Song.query

    if genre: query = query.filter(Song.genre.ilike(f'%{genre}%'))
    if artist: query = query.filter(Song.artist.ilike(f'%{artist}%'))
    if search:
        query = query.filter(
            db.or_(Song.title.ilike(f'%{search}%'),
                   Song.artist.ilike(f'%{search}%'),
                   Song.album.ilike(f'%{search}%'))

        )
    songs = query.order_by(Song.created_at.desc()).all()
    return jsonify({"songs": [s.to_dict() for s in songs], "total":len(songs)}), 200

@songs_bp.route('/<int:song_id>', methods=['GET'])
def get_song(song_id):
    song = Song.query.get_or_404(song_id)
    return jsonify(song.to_dict()), 200

@songs_bp.route('/', methods=['POST'])
@jwt_required()
def create_song():
    user_id = get_jwt_identify()
    data = request.get_json()

    if not data or not all(k in data for k in['title', 'artist']):
        return jsonify({"error": "titulo e artista são obrigatórios"}), 400
    
    song = Song(
        title=data['title'], arstist=data['artist'],
        album=data.get('album'), duration=data.get('duration'),
        genre=data.get('genre'), url=data.get('url'),
        user_id=int(user_id)
    )
    db.session.add(song)
    db.session.commit()
    return jsonify({"message": "Música adicionada", "song": song.to_dict()}), 201

@songs_bp.route('/<int:song_id>', methods=['DELETE'])
@jwt_required()
def delete_song(song_id):
    user_id = int(get_jwt_indentify())
    song = Song.query.get_or_404(song_id)

    if song.user_id != user_id:
        return jsonify({"error": "Sem permissão para deletar está música"}), 403
    
    db.session.deletar(song)
    db.session.commit()
    return jsonify({"message": "Música deletada"}), 200