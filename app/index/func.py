from flask import session
from peewee import JOIN
from app.models.links import Link
from app.models.types import TypeNews
from app.models.types import TypeLinks
from app.models.news import News


def get_links_for_base():
    ood = list(Link.select().where((Link.typelink.typecode == 1) &
                                   (Link.isactive == 1) &
                                   (TypeLinks.isactive == 1))
               .join(TypeLinks).order_by(Link.position, Link.linkname))
    zdrav = list(Link.select().where((TypeLinks.typecode == 2) &
                                     (Link.isactive == 1) &
                                     (TypeLinks.isactive == 1))
                 .join(TypeLinks).order_by(Link.position, Link.linkname))
    dop = list(Link.select().where((TypeLinks.typecode == 3) &
                                   (Link.isactive == 1) &
                                   (TypeLinks.isactive == 1))
               .join(TypeLinks).order_by(Link.position, Link.linkname))
    files = list(Link.select().where((TypeLinks.typecode == 4) &
                                     (Link.isactive == 1) &
                                     (TypeLinks.isactive == 1))
                 .join(TypeLinks).order_by(Link.position, Link.linkname))
    video = list(Link.select().where((TypeLinks.typecode == 5) &
                                     (Link.isactive == 1) &
                                     (TypeLinks.isactive == 1))
                 .join(TypeLinks).order_by(Link.position, Link.linkname))

    linksall = {'ood': ood,
                'zdrav': zdrav,
                'dop': dop,
                'files': files,
                'video': video
                }
    return linksall


def get_types_news():
    sel = TypeNews.select().where(TypeNews.isactive == 1)
    types = list(sel)
    return types


def get_news(typenews=None):
    # print(session.user.roles)
    if typenews:
        if session.user and 'SYS' in session.user.roles:
            sel = (News
                   .select()
                   .where((TypeNews.isactive == 1) &
                          (TypeNews.id == typenews))
                   .join(TypeNews, JOIN.LEFT_OUTER,
                         on=(News.typenews_id == TypeNews.id))
                   .order_by(News.createdate.desc()))
        else:
            sel = (News
                   .select()
                   .where((News.isactive == 1) &
                          (TypeNews.isactive == 1) &
                          (TypeNews.id == typenews))
                   .join(TypeNews, JOIN.LEFT_OUTER,
                         on=(News.typenews_id == TypeNews.id))
                   .order_by(News.createdate.desc()))
    else:
        if session.user and 'SYS' in session.user.roles:
            sel = (News
                   .select()
                   .where(TypeNews.isactive == 1)
                   .join(TypeNews, JOIN.LEFT_OUTER,
                         on=(News.typenews_id == TypeNews.id))
                   .order_by(News.createdate.desc()))
        else:
            sel = (News
                   .select()
                   .where((News.isactive == 1) &
                          (TypeNews.isactive == 1))
                   .join(TypeNews, JOIN.LEFT_OUTER,
                         on=(News.typenews_id == TypeNews.id))
                   .order_by(News.createdate.desc()))

    return sel
