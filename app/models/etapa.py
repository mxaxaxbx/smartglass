from app import db

class Etapa(db.Model):

  __tablename__ = 'etapas'
  __table_args__ = {'schema': 'smartglass'}  # Esquema específico

  idetapa = db.Column(db.Integer, primary_key=True)
  areaid = db.Column(db.Integer, db.ForeignKey('smartglass.areas.idarea'), nullable=False)
  nombre = db.Column(db.String(120), nullable=False)
  etapafinal = db.Column(db.Boolean, nullable=False)
  created = db.Column(db.Integer, nullable=False)
  update = db.Column(db.Integer, nullable=False)
  hsProcesos = db.relationship("HistorialProceso", backref='historialproceso', lazy=True)

  def save(self):
    db.session.add(self)
    db.session.commit()

  def serialize(self):
    return {
      'idetapa': str(self.idetapa),
      'areaid': str(self.areaid),
      'nombre': self.nombre,
      'etapafinal': self.etapafinal,
      'update': self.update,
      'created': self.created,
      #'hsProcesos': [lo_hProceso.serialize() for lo_hProceso in self.hsProcesos]
    }
  
  def put(self):
    db.session.commit()
