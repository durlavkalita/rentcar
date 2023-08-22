from app import db
from app.business import bp
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Business, Car
from app import redis_client
import json

@bp.route("/register", methods=['POST'])
@jwt_required()
def register_business():
  try:
    current_user_id = get_jwt_identity()
    data = request.json

    name = data.get("name")
    description = data.get("description")
    location = data.get("location")

    if not name or not location:
      return jsonify(message="Name and location are required fields"), 400

    new_business = Business(
      name = name,
      description = description,
      owner_id = current_user_id,
      location = location
    )

    db.session.add(new_business)
    db.session.commit()

    redis_client.delete('business_list')
    
    return jsonify(message="Business registered successfully"), 201
  except Exception as e:
    return jsonify(error=str(e)), 500

@bp.route("/", methods=['GET'])
def get_all_business():
  try:
    cached_data = redis_client.get('business_list')
    if cached_data:
      retrieved_list = json.loads(cached_data)
      return jsonify(retrieved_list), 200
    businesses = Business.query.all()
    business_list = []
    for business in businesses:
      business_data = {
        "id": business.id,
        "name": business.name,
        "description": business.description,
        "location": business.location,
        "owner_id": business.owner_id
      }
      business_list.append(business_data)
    json_business_list = json.dumps(business_list)
    redis_client.setex('business_list', 3600, json_business_list)
    return jsonify(business_list), 200
  except Exception as e:
    return jsonify(error=str(e)), 500

@bp.route("/<int:id>", methods=['GET'])
def get_business_by_id(id):
  try:
    business = db.session.get(Business, id)
    if business:
      business_data = {
        "id": business.id,
        "name": business.name,
        "description": business.description,
        "location": business.location,
        "owner_id": business.owner_id
      }
      return jsonify(business_data), 200
    else:
      return jsonify(message="business not found"), 404
  except Exception as e:
    return jsonify(error=str(e)), 500
  
@bp.route("/<int:id>/cars", methods=["GET"])
def get_cars_by_business(id):
  try:
    cars = Car.query.filter_by(business_id = id)
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