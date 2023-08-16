from app import db
from app.car import bp
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Car, Business, Booking
from flask import request, jsonify
from datetime import datetime

@bp.route("/create", methods=['POST'])
@jwt_required()
def create_car():
  try:
    current_user_id = get_jwt_identity()
    data = request.json

    current_user_business = Business.query.filter_by(owner_id = current_user_id).first()
    if not current_user_business:
      return jsonify(message="Register a business first"), 400

    brand = data.get("brand")
    model = data.get("model")
    year = data.get("year")
    color = data.get("color")
    license_plate = data.get("license_plate")
    price_per_day = data.get("price_per_day")
    available = data.get("available")
    business_id = current_user_business

    new_car = Car(
      brand = brand,
      model = model,
      year = year,
      color = color,
      license_plate = license_plate,
      price_per_day = price_per_day,
      available = available,
      business_id = current_user_business.id
    )

    db.session.add(new_car)
    db.session.commit()

    return jsonify(message="Car created successfully"), 201
  except Exception as e:
    return jsonify(error=str(e)), 500

@bp.route("/", methods=["GET"])
def get_all_cars():
  try:
    cars = Car.query.all()
    car_list = []
    for car in cars:
      car_data = {
        "id": car.id,
        "brand": car.brand,
        "model": car.model,
        "year": car.year,
        "color": car.color,
        "license_plate": car.license_plate,
        "price_per_day": car.price_per_day,
        "available": car.available,
        "business_id": car.business.id
      }
      car_list.append(car_data)
    return jsonify(car_list), 200
  except Exception as e:
    return jsonify(error=str(e)), 500

@bp.route("/<int:id>", methods=['GET'])
def get_car_by_id(id):
  try:
    car = Car.query.get(id)
    if car:
      car_data = {
        "id": car.id,
        "brand": car.brand,
        "model": car.model,
        "year": car.year,
        "color": car.color,
        "license_plate": car.license_plate,
        "price_per_day": car.price_per_day,
        "available": car.available,
        "business_id": car.business.id
      }
      return jsonify(car_data), 200
    else:
      return jsonify(message="car not found"), 404
  except Exception as e:
    return jsonify(error=str(e)), 500
  
@bp.route("/<int:id>/bookings/create", methods=["POST"])
@jwt_required()
def book_car_by_id(id):
  try:
    current_user_id = get_jwt_identity()
    car = Car.query.get(id)
    if not car:
      return jsonify(message="Car not found"), 404
    elif car.available != True:
      return jsonify(message="car not available"), 403

    data = request.json
    pickup_date = datetime.strptime(data.get("pickup_date"), "%Y-%m-%d")
    return_date = datetime.strptime(data.get("return_date"), "%Y-%m-%d")

    rental_price_per_day = car.price_per_day

    # Calculate the number of rental days
    rental_days = (return_date - pickup_date).days + 1

    # Calculate the total price
    total_price = rental_price_per_day * rental_days

    new_booking = Booking(
        user_id=current_user_id,
        car_id=id,
        pickup_date=pickup_date,
        return_date=return_date,
        total_price=total_price
    )

    db.session.add(new_booking)
    db.session.commit()

    return jsonify(message="Booking created successfully"), 201
  except Exception as e:
    return jsonify(error=str(e)), 500

@bp.route("/<int:id>/bookings", methods=['GET'])
def get_bookings_by_car_id(id):
  try:
    car = Car.query.get(id)
    if not car:
      return jsonify(message="Car not found"), 404
    bookings = Booking.query.filter_by(car_id = id)
    booking_list = []
    for booking in bookings:
      booking_data = {
        "id": booking.id,
        "user": booking.user.first_name,
        "car": booking.car.brand,
        "pickup_date": booking.pickup_date,
        "return_date": booking.return_date,
        "total_price": booking.total_price,
        "created_at": booking.created_at
      }
      booking_list.append(booking_data)
    return jsonify(booking_list), 200
  except Exception as e:
    return jsonify(error=str(e)), 500

@bp.route("/<int:id>/edit", methods=['PUT'])
@jwt_required()
def edit_car_by_id(id):
  try:
    current_user_id = get_jwt_identity()
    car = Car.query.get(id)
    if not car:
      return jsonify(message="Car not found"), 404
    if car.business.owner_id != current_user_id:
      return jsonify(message="Not authorized to update car details"), 403
    data = request.json
    
    car.brand = data.get("brand", car.brand)
    car.model = data.get("model", car.model)
    car.year = data.get("year", car.year)
    car.color = data.get("color", car.color)
    car.available = data.get("available", car.available)
    car.price_per_day = data.get("price_per_day", car.price_per_day)
    db.session.commit()

    return jsonify(message="Car details updated successfully"), 200
  except Exception as e:
    return jsonify(error=str(e)), 500

@bp.route("/<int:id>", methods=['DELETE'])
@jwt_required()
def delete_car_by_id(id):
  try:
    current_user_id = get_jwt_identity()
    car = Car.query.get(id)
    if not car:
      return jsonify(message="Car not found"), 404
    if car.business.owner_id != current_user_id:
      return jsonify(message="Unauthorized"), 403
    db.session.delete(car)
    db.session.commit()
    return jsonify(message="Car deleted successfully"), 200
  except Exception as e:
    return jsonify(error=str(e)), 500
  