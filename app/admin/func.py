from peewee import JOIN
from app.models.users import User
from app.models.types import TypeLinks, TypeNews
from app.models.links import Link

# возврат всего списка пользователей
def find_all_users():
    sel = (User
          .select()
          .order_by(User.username)
          .namedtuples())
    
    users = []
    i=1
    for user in sel:
        users.append(
            {'id': user.id,
             'ind':i,
             'username': user.username,
             }
        )
        i=i+1

    return users

# возврат всего списка типов
def find_all_types(tab):
    if tab == 'news':
        table = TypeNews
    else:
        table = TypeLinks
    
    sel = (table
          .select()
          .order_by(table.typecode)
          .namedtuples())
    
    types = []
    for t in sel:
        types.append(
            {'id': t.id,
             'ind': t.typecode,
             'typename': t.typename,
             'isactive': t.isactive
             }
        )
    return types

# возврат всего списка ссылок
def find_all_links():
    sel = (Link
          .select(
          Link.id,
          Link.linkname,
          Link.fullname,
          TypeLinks.typename.alias('typelink'))
          .join(TypeLinks, JOIN.LEFT_OUTER, 
                on=(TypeLinks.id == Link.typelink_id))
          .order_by(Link.typelink, Link.linkname)
          .namedtuples())
    
    links = []
    for l in sel:
        links.append(
            {'id': l.id,
             'linkname': l.linkname,
             'fullname': l.fullname,
             'typelink': l.typelink,
             }
        )

    return links
