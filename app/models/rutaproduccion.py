from app import db

class RutaProduccion(db.Model):

  __tablename__ = 'rutasproduccion'
  __table_args__ = {'schema': 'smartglass'}  # Esquema específico

  idrutaprdcion = db.Column(db.Integer, primary_key=True)
  nombre = db.Column(db.String(120), nullable=False)
  created = db.Column(db.Integer, nullable=False)
  update = db.Column(db.Integer, nullable=False)

  def save(self):
    db.session.add(self)
    db.session.commit()

  def serialize(self):
    return {
      'idrutaprdcion': str(self.idrutaprdcion),
      'nombre': self.nombre,
      'update': self.update,
      'created': self.created
    }
  
  def put(self):
    db.session.commit()
