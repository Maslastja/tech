import peewee as pw
from config.database import db
from app.models.types import TypeNews


class News(db.Model):
    name = pw.CharField(150, null=False)
    user = pw.IntegerField(null=False)
    typenews = pw.ForeignKeyField(TypeNews, null=False)
    isactive = pw.BooleanField(default=True)
    text = pw.TextField(null=False)
    createdate = pw.DateTimeField()
    changedate = pw.DateTimeField()

    class Meta:
        db_table = 'news'
        order_by = ('createdate')

    def __str__(self):
        return self.name
