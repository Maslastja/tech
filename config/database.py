from peewee import Model
from playhouse.flask_utils import FlaskDB, get_object_or_404

class BaseModelClass(Model):
    # поиск по id
    @classmethod
    def get_by_id(self, id):
        result = get_object_or_404(self, self.id == id)
        return result

class MyFlaskBD(FlaskDB):
    def connect_db(self):
        if self.database.is_closed():
            self.database.connect()
    
    def close_db(self, exc):
        if not self.database.is_closed():
            self.database.close()
    
    
db = MyFlaskBD(model_class=BaseModelClass)


