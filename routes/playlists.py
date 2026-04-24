from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Playlist, Song

playlists_bp = Blueprint('playlists', __name__)

@playlists_bp.route('/', methods=['GET'])
def get_playlists():
    playlists = Playlist.query.order_by(Playlist.created_at.desc()).all()
    return jsonify({"playlists": [p.to_dict() for p in playlists]}), 200


@playlists_bp.route('/', methods=['POST'])
@jwt_required()
def create_playlist():
    user_id = int(get_jwt_identity())
    data    = request.get_json()

    if not data or 'name' not in data:
        return jsonify({"error": "name é obrigatório"}), 400

    playlist = Playlist(name=data['name'],
                        description=data.get('description', ''),
                        user_id=user_id)
    db.session.add(playlist)
    db.session.commit()
    return jsonify({"message": "Playlist criada!", "playlist": playlist.to_dict()}), 201


@playlists_bp.route('/<int:playlist_id>/songs', methods=['POST'])
@jwt_required()
def add_song_to_playlist(playlist_id):
    user_id  = int(get_jwt_identity())
    playlist = Playlist.query.get_or_404(playlist_id)

    if playlist.user_id != user_id:
        return jsonify({"error": "Sem permissão"}), 403

    data    = request.get_json()
    song_id = data.get('song_id')
    song    = Song.query.get_or_404(song_id)

    if song in playlist.songs:
        return jsonify({"error": "Música já está na playlist"}), 409

    playlist.songs.append(song)
    db.session.commit()
    return jsonify({"message": "Música adicionada à playlist!", "playlist": playlist.to_dict()}), 200