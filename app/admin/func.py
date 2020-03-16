from flask import jsonify
from app.models.types import TypeLinks, TypeNews
from app.models.links import Link


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
        types.append({'id': t.id,
                      'ind': t.typecode,
                      'typename': t.typename,
                      'isactive': t.isactive})
    return types


# возврат всего списка ссылок ajax
def links_ajax(typelink):
    sel = (Link
           .select(Link.id,
                   Link.linkname,
                   Link.fullname,
                   Link.isactive,
                   TypeLinks.typename.alias('typelink'))
           .join(TypeLinks))

    if typelink != '':
        sel = sel.where(TypeLinks.id == typelink)
    sel = (sel
           .order_by(Link.typelink, Link.position, Link.linkname)
           .namedtuples())

    links = []
    for l in sel:
        links.append({'id': l.id,
                      'linkname': l.linkname,
                      'fullname': l.fullname,
                      'typelink': l.typelink,
                      'isactive': l.isactive})
    return jsonify(links)
