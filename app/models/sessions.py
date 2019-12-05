import peewee as pw
from flask import session
from config.database import db
from app.models.users import User

class SessionsStore(db.Model):
       token = pw.CharField(primary_key = True)
       user = pw.ForeignKeyField(User, null=False)
       DateCreate = pw.DateTimeField()
       DateLastReq = pw.DateTimeField()
       
       class Meta:
              db_table = 'sessions'
        
       
       
