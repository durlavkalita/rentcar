from app.auth import bp
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user import User
from app import db

@bp.route('/register', methods=['POST'])
def register():
  data = request.json

  email = data.get("email")
  password = data.get("password")
  first_name = data.get("first_name")
  last_name = data.get("last_name")
  phone_number = data.get("phone_number")

  existing_user =  User.query.filter_by(email = email).first()
  if existing_user:
    return jsonify(message = "User already exists."), 400

  new_user = User(
    email=email,
    password=password,
    first_name=first_name,
    last_name=last_name,
    phone_number=phone_number
    )

  db.session.add(new_user)
  db.session.commit()

  access_token = create_access_token(identity=new_user.id)

  return jsonify(message="User registered successfully", access_token=access_token), 201

@bp.route('/login', methods=['POST'])
def login():
  data = request.json

  email = data.get("email")
  password = data.get("password")

  user = User.query.filter_by(email = email).first()
  if user is None or not user.check_password(password):
    return jsonify(message="Invalid Username or password"), 400
  access_token = create_access_token(identity=user.id)

  return jsonify(message="User logged in successfully", access_token=access_token), 200