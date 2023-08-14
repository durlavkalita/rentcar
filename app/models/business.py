from app import db

class Business(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  description = db.Column(db.Text)
  owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  location = db.Column(db.String(200))

  owner = db.relationship("User", back_populates="businesses")
  cars = db.relationship("Car", back_populates="business")

  def __repr__(self):
    return f"<Business {self.name}>"
