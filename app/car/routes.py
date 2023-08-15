from app import db
from app.car import bp
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Car, Business
from flask import request, jsonify

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
  
