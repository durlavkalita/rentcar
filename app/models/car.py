from app import db

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer)
    color = db.Column(db.String(50))
    license_plate = db.Column(db.String(20), nullable=False, unique=True)
    price_per_day = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    available = db.Column(db.Boolean, default=True)
    business_id = db.Column(db.Integer, db.ForeignKey("business.id"), nullable=False)

    business = db.relationship("Business", back_populates="cars")
    bookings = db.relationship("Booking", back_populates="car")

    def __repr__(self):
        return f"<Car {self.brand} {self.model}>"