from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    #Validação básica
    if not data or not all(k in data for k in['username','email','password']):
        return jsonify({"error": "Campos obrigatórios: username, email, password"}), 400
    #Verificar se o usuário já existe
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "E-mail já cadastrado"}), 409
    # Cria o usuário com senha criptografada
    user = User(
        username=data['username'],
        email=data['email'],
        password=generate_password_hash(data['password'])
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Usuário criado!", "user": user.to_dict()}), 201

@auth_bp.route('login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data.get('email')).first()

    if not user or not check_password_hash(user.password, data.get('password', '')):
        return jsonify({"error": "Credenciais inválidas"}), 401
    
    #Gera o token JWT
    token = create_access_token(identify=str(user.id))

    return jsonify({
        "message": "Login realizado!",
        "token": token,
        "user": user.to_dict()
    }), 200