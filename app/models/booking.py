from app import db
from datetime import datetime

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey("car.id"), nullable=False)
    pickup_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="bookings")
    car = db.relationship("Car", back_populates="bookings")

    def __repr__(self):
        return f"<Booking {self.id}>"
