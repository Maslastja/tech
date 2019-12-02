from peewee import JOIN
from app.models.links import Link
from app.models.types import TypeNews
from app.models.types import TypeLinks
from app.models.news import News

def get_links_for_base():
    ood = list(Link.select().where(Link.typelink.typecode == 1)
               .join(TypeLinks, JOIN.LEFT_OUTER,
                     on=(Link.typelink_id == TypeLinks.id)))
    zdrav = list(Link.select().where(TypeLinks.typecode == 2)
               .join(TypeLinks, JOIN.LEFT_OUTER,
                     on=(Link.typelink_id == TypeLinks.id)))
    dop = list(Link.select().where(TypeLinks.typecode == 3)
               .join(TypeLinks, JOIN.LEFT_OUTER,
                     on=(Link.typelink_id == TypeLinks.id)))
    files = list(Link.select().where(TypeLinks.typecode == 4)
               .join(TypeLinks, JOIN.LEFT_OUTER,
                     on=(Link.typelink_id == TypeLinks.id)))
    video = list(Link.select().where(TypeLinks.typecode == 5)
               .join(TypeLinks, JOIN.LEFT_OUTER,
                     on=(Link.typelink_id == TypeLinks.id)))
    
    linksall = {'ood': ood,
                'zdrav': zdrav,
                'dop': dop,
                'files': files,
                'video': video
                }
    
    return linksall

def get_types_news():
    sel = TypeNews.select().where(TypeNews.isactive == True)
    types = list(sel)
    return types

def get_news(typenews=None):
    if typenews:
        sel = (News
               .select()
               .where((TypeNews.isactive == True) &
                      (TypeNews.id == typenews))
               .join(TypeNews, JOIN.LEFT_OUTER, 
                     on=(News.typenews_id == TypeNews.id))
               .order_by(News.createdate.desc()))
    else:
        sel = (News
               .select()
               .where(TypeNews.isactive == True)
               .join(TypeNews, JOIN.LEFT_OUTER, 
                     on=(News.typenews_id == TypeNews.id))
               .order_by(News.createdate.desc()))
    
    news = list(sel)
    return news
