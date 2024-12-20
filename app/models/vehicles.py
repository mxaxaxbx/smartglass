from app import db

class Vehicle(db.Model):

  __tablename__ = 'vehicles'

  id = db.Column(db.Integer, primary_key=True)
  brand = db.Column(db.String(120), nullable=False)
  model = db.Column(db.String(120), nullable=False)
  year = db.Column(db.Integer, nullable=False)

  def save(self):
    db.session.add(self)
    db.session.commit()

  def serialize(self):
    return {
      'id': str(self.id),
      'brand': self.brand,
      'model': self.model,
      'year': self.year
    }
