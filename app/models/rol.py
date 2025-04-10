from app import db

class Rol(db.Model):

  __tablename__ = 'roles'
  __table_args__ = {'schema': 'smartglass'}  # Esquema específico

  idrol = db.Column(db.Integer, primary_key=True)
  nombre = db.Column(db.String(120), nullable=False)
  endpoint = db.Column(db.String(120), nullable=False)
  created = db.Column(db.Integer, nullable=False)
  update = db.Column(db.Integer, nullable=False)

  def serialize(self):
    return {
      'idrol': str(self.idrol),
      'nombre': self.nombre,
      'endpoint': self.endpoint,
      'created': self.created,
      'update': self.update
    }
  
  def save(self):
    db.session.add(self)
    db.session.commit()
  
  def put(self):
    db.session.commit()
