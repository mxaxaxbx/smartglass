from app import db

class PartTypes(db.Model):

  __tablename__ = 'part_types'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)

  def save(self):
    db.session.add(self)
    db.session.commit()

  def serialize(self):
    return {
      'id': str(self.id),
      'name': self.name
    }
