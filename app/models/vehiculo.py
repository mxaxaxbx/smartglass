from app import db

class Vehiculo(db.Model):

  __tablename__ = 'vehiculos'
  __table_args__ = {'schema': 'smartglass'}  # Esquema específico

  idvehiculo = db.Column(db.Integer, primary_key=True)
  marca = db.Column(db.String(120), nullable=False)
  modelo = db.Column(db.String(120), nullable=False)
  year_ini_prod = db.Column(db.Integer, nullable=False)
  year_fin_prod = db.Column(db.Integer, nullable=False)
  created = db.Column(db.Integer, nullable=False)
  update = db.Column(db.Integer, nullable=False)

  def serialize(self):
    return {
      'idvehiculo': str(self.idvehiculo),
      'marca': self.marca,
      'modelo': self.modelo,
      'year_ini_prod': self.year_ini_prod,
      'year_fin_prod': self.year_fin_prod,
      'created': self.created,
      'update': self.update
    }
  
  def save(self):
    db.session.add(self)
    db.session.commit()
     
  def put(self):
    db.session.commit()
