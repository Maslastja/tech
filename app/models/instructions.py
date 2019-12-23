import peewee as pw
from config.database import db


class Instruction(db.Model):
    name = pw.CharField(150, null=False)
    isactive = pw.BooleanField(default=True)
    text = pw.TextField(null=False)
    user = pw.IntegerField(null=False)
    createdate = pw.DateTimeField()
    changedate = pw.DateTimeField()

    class Meta:
        db_table = 'instructions'

    def __str__(self):
        return self.name
