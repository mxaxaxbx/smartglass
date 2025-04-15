from app import db

class TipoSolicitud(db.Model):

  __tablename__ = 'tipos_solicitud'
  __table_args__ = {'schema': 'smartglass'}  # Esquema específico

  idtposol = db.Column(db.Integer, primary_key=True)
  nombre = db.Column(db.String(120), nullable=False)
  created = db.Column(db.Integer, nullable=False)
  update = db.Column(db.Integer, nullable=False)

  def save(self):
    db.session.add(self)
    db.session.commit()

  def serialize(self):
    return {
      'idtposol': str(self.idtposol),
      'nombre': self.nombre,
      'update': self.update,
      'created': self.created
    }
  
  def put(self):
    db.session.commit()
