import peewee as pw
from config.database import db
from app.models.users import User
from app.models.types import TypeLinks

class Link(db.Model):
       id = pw.PrimaryKeyField(null=False)
       linkname = pw.CharField(max_length=20, null=False)
       fullname = pw.CharField(max_length=150,null=False)
       typelink = pw.ForeignKeyField(TypeLinks, null=False)
       user = pw.ForeignKeyField(User, null=False)
       createdate = pw.DateTimeField()
       changedate = pw.DateTimeField()
       
       class Meta:
              db_table = "links"
              order_by = ('id',)
       
       def __str__(self):
              return self.linkname
