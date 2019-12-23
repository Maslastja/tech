import peewee as pw
from config.database import db


class Types(db.Model):
    typename = pw.CharField(50, null=False)
    typecode = pw.IntegerField()    isactive = pw.BooleanField(default=True)

    def __str__(self):
        return self.typename


class TypeLinks(Types):
    class Meta:
        db_table = 'typelinks'
        order_by = ('id')


class TypeNews(Types):
    class Meta:
        db_table = 'typenews'
        order_by = ('id')
