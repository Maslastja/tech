import peewee as pw
from config.database import db
from app.models.types import TypeLinks


class Link(db.Model):
    linkname = pw.CharField(20, null=False)
    fullname = pw.CharField(150, null=False)
    typelink = pw.ForeignKeyField(TypeLinks, null=False)
    isactive = pw.BooleanField(default=True)
    user = pw.IntegerField(null=False)
    createdate = pw.DateTimeField()
    changedate = pw.DateTimeField()

    class Meta:
        # db_table = 'links'
        table_name = 'links'
        order_by = ('id')

    def __str__(self):
        return self.linkname
