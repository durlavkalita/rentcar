from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password_hash = db.Column(db.String(128), nullable=False)
  first_name = db.Column(db.String(50), nullable=False)
  last_name = db.Column(db.String(50), nullable=False)
  phone_number = db.Column(db.String(20))
  date_joined = db.Column(db.DateTime, default=datetime.utcnow)

  def __init__(self, email, password, first_name, last_name, phone_number=None):
    self.email = email
    self.password_hash = generate_password_hash(password)
    self.first_name = first_name
    self.last_name = last_name
    self.phone_number = phone_number

  def __repr__(self):
    return '<User {} {}>'.format(self.first_name, self.last_name)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)