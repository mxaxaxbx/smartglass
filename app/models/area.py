from app import db

class Area(db.Model):

  __tablename__ = 'areas'
  __table_args__ = {'schema': 'smartglass'}  # Esquema específico

  idarea = db.Column(db.Integer, primary_key=True)
  nombre = db.Column(db.String(120), nullable=False)
  created = db.Column(db.Integer, nullable=False)
  update = db.Column(db.Integer, nullable=False)
  etapas = db.relationship("Etapa", backref='etapas', lazy=True)

  def save(self):
    db.session.add(self)
    db.session.commit()

  def serialize(self):
    return {
      'idarea': str(self.idarea),
      'nombre': self.nombre,
      'update': self.update,
      'created': self.created,
      #'etapas': [lo_etapa.serialize() for lo_etapa in self.etapas]
    }
  
  def put(self):
    db.session.commit()
