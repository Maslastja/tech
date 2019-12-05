import peewee as pw
from werkzeug.security import generate_password_hash, check_password_hash
from config.database import db

class User(db.Model):
       username = pw.CharField(15, null=False)
       password = pw.CharField(124)
       isadmin = pw.BooleanField(default=False)
       isactive = pw.BooleanField(default=True)
       
       class Meta:
              db_table = 'users'
              order_by = ('id')
       
       @property
       def pwd(self):
              raise AttributeError('not read pwd')
       
       @pwd.setter
       def pwd(self, password):
              self.password = generate_password_hash(password)

       def check_password(self, password):
              return check_password_hash(self.password, password)

