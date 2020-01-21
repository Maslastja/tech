import peewee as pw
from config.database import db


class Phones(db.Model):
    idfil = pw.CharField(15, null=False)
    idotd = pw.CharField(30)
    typeotd = pw.CharField(15, null=False)
    nameabon = pw.CharField(100, null=False)
    numberin = pw.CharField(15, null=True)
    numberout = pw.CharField(15, null=True)
    email = pw.CharField(50, null=True)
    isgeneral = pw.BooleanField(default=False)
    isactive = pw.BooleanField(default=True)
    comment = pw.CharField(100, null=True)

    class Meta:
        db_table = 'phones'
        order_by = ('idotd', 'isgeneral', 'namefil')

    def __str__(self):
        return (f'{self.nameabon} внутренний {self.numberin} внешний'
                f' {self.numberout}')
