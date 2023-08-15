from app import db
from app.business import bp
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Business

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

    return jsonify(message="Business registered successfully"), 201
  except Exception as e:
    return jsonify(error=str(e)), 500

@bp.route("/", methods=['GET'])
def get_all_business():
  try:
    businesses = Business.query.all()
    business_list = []
    for business in businesses:
      business_data = {
        "id": business.id,
        "name": business.name,
        "description": business.description,
        "location": business.location
      }
      business_list.append(business_data)
    return jsonify(business_list), 200
  except Exception as e:
    return jsonify(error=str(e)), 500

