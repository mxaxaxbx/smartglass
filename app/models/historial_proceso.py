from app import db

class HistorialProceso(db.Model):

  __tablename__ = 'historialproceso'
  __table_args__ = {'schema': 'smartglass'}  # Esquema específico

  idhistorialprocso = db.Column(db.Integer, primary_key=True)
  estado = db.Column(db.String(120), nullable=False)
  fechaingreso = db.Column(db.Integer, nullable=False)
  fechasalida = db.Column(db.Integer, nullable=False)
  idetapa = db.Column(db.Integer, nullable=False)
  idproceso = db.Column(db.Integer, nullable=False)
  idusuario = db.Column(db.Integer, nullable=False)
  notas = db.Column(db.String(120), nullable=False)

  created = db.Column(db.Integer, nullable=False)
  update = db.Column(db.Integer, nullable=False)

  def serialize(self):
    return {
      'idhistorialprocso': str(self.idproceso),
      'estado': self.estado,
      'fechaingreso': self.fechaingreso,
      'fechasalida': self.fechasalida,
      'idetapa': str(self.idetapa),
      'idproceso': str(self.idproceso),
      'idusuario': str(self.idusuario),
      'notas': self.notas,
      'created': self.created,
      'update': self.update
    }
  
  def save(self):
    db.session.add(self)
    db.session.commit()
     
  def put(self):
    db.session.commit()
