from app import db

class Orden(db.Model):

  __tablename__ = 'ordenes'
  __table_args__ = {'schema': 'smartglass'}  # Esquema específico

  ordenid = db.Column(db.Integer, primary_key=True)
  fechapedido = db.Column(db.Integer, nullable=False)
  cliente = db.Column(db.String(120), nullable=False)
  torrecliente = db.Column(db.String(120), nullable=False)
  created = db.Column(db.Integer, nullable=False)
  update = db.Column(db.Integer, nullable=False)

  def serialize(self):
    return {
      'ordenid': str(self.ordenid),
      'fechapedido': self.fechapedido,
      'cliente': self.cliente,
      'torrecliente': self.torrecliente,
      'created': self.created,
      'update': self.update
    }
  
  def save(self):
    db.session.add(self)
    db.session.commit()
  
  def put(self):
    db.session.commit()
