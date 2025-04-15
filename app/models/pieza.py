from app import db

class Pieza(db.Model):

  __tablename__ = 'piezas'
  __table_args__ = {'schema': 'smartglass'}  # Esquema específico

  idpieza = db.Column(db.Integer, primary_key=True)
  ordenid = db.Column(db.Integer, nullable=False)
  idvehiculo = db.Column(db.Integer, nullable=False)
  idrutaprdccion = db.Column(db.Integer, nullable=False)
  espesorval = db.Column(db.Float, nullable=False)
  espesor_unidad = db.Column(db.String(120), nullable=False)
  fechaentrega = db.Column(db.Integer, nullable=False)
  idtpopieza = db.Column(db.Integer, nullable=False)
  idtposol = db.Column(db.Integer, nullable=False)

  created = db.Column(db.Integer, nullable=False)
  update = db.Column(db.Integer, nullable=False)

  def serialize(self):
    return {
      'idpieza': str(self.idpieza),
      'ordenid': self.ordenid,
      'idvehiculo': self.idvehiculo,
      'idrutaprdccion': self.idrutaprdccion,
      'espesorval': self.espesorval,
      'espesor_unidad': self.espesor_unidad,
      'fechaentrega': self.fechaentrega,
      'idtpopieza': self.idtpopieza,
      'idtposol': self.idtposol,
      'created': self.created,
      'update': self.update
    }
  
  def save(self):
    db.session.add(self)
    db.session.commit()
     
  def put(self):
    db.session.commit()
