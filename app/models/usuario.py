from app import db

class Usuario(db.Model):

  __tablename__ = 'usuarios'
  __table_args__ = {'schema': 'smartglass'}  # Esquema específico

  userid = db.Column(db.Integer, primary_key=True)
  primer_nombre = db.Column(db.String(120), nullable=False)
  segundo_nombre = db.Column(db.String(120), nullable=False)
  primer_apellido = db.Column(db.String(120), nullable=False)
  segundo_apellido = db.Column(db.String(120), nullable=False)
  active = db.Column(db.Boolean, nullable=False)
  superuser = db.Column(db.Boolean, nullable=False)
  created = db.Column(db.Integer, nullable=False)
  update = db.Column(db.Integer, nullable=False)
  lastlogin = db.Column(db.Integer, nullable=False)
  email = db.Column(db.String(120), nullable=False)
  password = db.Column(db.String(120), nullable=False)
  idrol = db.Column(db.Integer, nullable=False)
  idarea = db.Column(db.Integer, nullable=False)

  def serialize(self):
    return {
      'userid': str(self.userid),
      'primer_nombre': self.primer_nombre,
      'segundo_nombre': self.segundo_nombre,
      'primer_apellido': self.primer_apellido,
      'segundo_apellido': self.segundo_apellido,
      'email': self.email,
      'idrol': self.idrol,
      'idarea': self.idarea,
      'active': self.active,
      'superuser': self.superuser,
      'created': self.created,
      'update': self.update,
      'lastlogin': self.lastlogin
    }
  
  def save(self):
    db.session.add(self)
    db.session.commit()
  
  def put(self):
    db.session.commit()
