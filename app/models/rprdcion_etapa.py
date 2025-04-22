from app import db

class RPrdcion_Etapas(db.Model):

  __tablename__ = 'rprdcion_etapas'
  __table_args__ = {'schema': 'smartglass'}  # Esquema específico

  id_rprdcion_etapa = db.Column(db.Integer, primary_key=True)
  id_rutprod = db.Column(db.Integer, nullable=False)
  idetapa = db.Column(db.Integer, nullable=False)
  orden = db.Column(db.Integer, nullable=False)
  created = db.Column(db.Integer, nullable=False)
  update = db.Column(db.Integer, nullable=False)

  def save(self):
    db.session.add(self)
    db.session.commit()

  def serialize(self):
    return {
      'idetid_rprdcion_etapaapa': str(self.id_rprdcion_etapa),
      'id_rutprod': str(self.id_rutprod),
      'idetapa': str(self.idetapa),
      'orden': self.orden,
      'update': self.update,
      'created': self.created
    }
  
  def put(self):
    db.session.commit()
