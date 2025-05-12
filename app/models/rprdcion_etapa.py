from app import db
from app.models.etapa import Etapa

class RPrdcion_Etapas(db.Model):

  __tablename__ = 'rprdcion_etapas'
  __table_args__ = {'schema': 'smartglass'}  # Esquema específico

  id_rprdcion_etapa = db.Column(db.Integer, primary_key=True)
  id_rutprod = db.Column(db.Integer, nullable=False)
  idetapa = db.Column(db.Integer, db.ForeignKey('smartglass.etapas.idetapa'), nullable=False)
  orden = db.Column(db.Integer, nullable=False)
  created = db.Column(db.Integer, nullable=False)
  update = db.Column(db.Integer, nullable=False)
  etapa = db.relationship('Etapa', backref='rprdcion_etapas', lazy=True)

  def save(self):
    db.session.add(self)
    db.session.commit()

  def serialize(self):
    return {
      'id_rprdcion_etapa': str(self.id_rprdcion_etapa),
      'id_rutprod': str(self.id_rutprod),
      'idetapa': str(self.idetapa),
      'orden': self.orden,
      'update': self.update,
      'created': self.created,
      'n_etapa': self.etapa.nombre
    }
  
  def put(self):
    db.session.commit()
