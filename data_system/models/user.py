#from data_system.extensions import db
#from werkzeug.security import generate_password_hash, check_password_hash
#
#class User(db.Model):
#    __tablename__ = 'user'
#
#    id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.String(80), nullable=False, unique=True)
#    password_hash = db.Column(db.String(200))
#   #is_active = db.Column(db.Boolean(), default=False)
#    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
#    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
#
#    @classmethod
#    def get_by_username(cls, username):
#        return cls.query.filter_by(username=username).first()
#    
#    def set_password(self, password):
#        self.password_hash = generate_password_hash(password)
#
#    def validate_password(self, password):
#        return check_password_hash(self.password_hash, password)
