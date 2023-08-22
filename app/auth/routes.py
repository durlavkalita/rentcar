from app.auth import bp
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app import db

@bp.route('/register', methods=['POST'])
def register():
  try:
    data = request.json

    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    phone_number = data.get("phone_number")
    
    if not email or not password or not first_name or not last_name:
      return jsonify(message="Please fill all required fields"), 400

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

  except Exception as e:
    return jsonify(error=str(e)), 500

@bp.route('/login', methods=['POST'])
def login():
  try:
    data = request.json

    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
      return jsonify(message="Email and password are required fields"), 400

    user = User.query.filter_by(email = email).first()
    if user is None or not user.check_password(password):
      return jsonify(message="Invalid Username or password"), 400
    access_token = create_access_token(identity=user.id)

    return jsonify(message="User logged in successfully", access_token=access_token), 200
  except Exception as e:
    return jsonify(error=str(e)), 500

@bp.route("/profile", methods=['GET'])
@jwt_required()
def get_user_profile():
  current_user_id = get_jwt_identity()
  try:
    user = db.session.get(User, current_user_id)
    if user:
      user_data = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number
      }
      return jsonify(user_data), 200
    else:
      return jsonify(message="user not found"), 404
  except Exception as e:
    return jsonify(error=str(e)), 500

@bp.route("/profile/booking", methods=["GET"])
@jwt_required()
def get_profile_booking_list():
  try:
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    booking_list = []
    for booking in user.bookings:
      booking_data = {
        "pickup_date": booking.pickup_date,
        "return_date": booking.return_date,
        "car_id": booking.car_id,
        "total_price": booking.total_price,
        "created_at": booking.created_at
      }
      booking_list.append(booking_data)
    return jsonify(booking_list), 200
  except Exception as e:
    return jsonify(error=str(e)), 500