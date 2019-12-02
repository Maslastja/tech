import peewee as pw
from config.database import db
from app.models.users import User

class Instruction(db.Model):
       id = pw.PrimaryKeyField(null=False)
       name = pw.CharField(max_length=150, null=False)
       text = pw.CharField(null=False)
       user = pw.ForeignKeyField(User, null=False)
       createdate = pw.DateTimeField()
       changedate = pw.DateTimeField()
       
       class Meta:
              db_table = "instructions"
        
       def __str__(self):
              return self.name