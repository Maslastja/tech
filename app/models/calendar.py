import peewee as pw
from config.database import db

class Calendar(db.Model):
       day = pw.DateField(null=False)
       timestart = pw.TimeField(null=False)
       timeend = pw.TimeField(null=False)
       event = pw.TextField(300)
       resp = pw.CharField(100, null=True)
       comment = pw.CharField(null=True)
       
       class Meta:
              db_table = 'calendar'
        
       def __str__(self):
              return f'{self.day.strftime("%d.%m.%Y")} {self.event}'