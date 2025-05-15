from app import db

class Proceso(db.Model):

  __tablename__ = 'procesos'
  __table_args__ = {'schema': 'smartglass'}  # Esquema específico

  idproceso = db.Column(db.Integer, primary_key=True)
  idpieza = db.Column(db.Integer, db.ForeignKey('smartglass.piezas.idpieza'), nullable=False)
  estado = db.Column(db.String(120), nullable=False)
  fechainicial = db.Column(db.Integer, nullable=False)
  fechafinal = db.Column(db.Integer, nullable=False)
  notas = db.Column(db.String(120), nullable=False)
  reproceso = db.Column(db.Boolean, nullable=False)
  pieza = db.relationship('Pieza', backref='procesos', lazy=True)

  created = db.Column(db.Integer, nullable=False)
  update = db.Column(db.Integer, nullable=False)

  def serialize(self):
    return {
      'idproceso': str(self.idproceso),
      'idpieza': str(self.idpieza),
      'estado': self.estado,
      'fechainicial': self.fechainicial,
      'fechafinal': self.fechafinal,
      'notas': self.notas,
      'reproceso': self.reproceso,
      'created': self.created,
      'update': self.update,
      'pieza': self.pieza.serialize(),
    }
  
  def save(self):
    db.session.add(self)
    db.session.commit()
     
  def put(self):
    db.session.commit()
