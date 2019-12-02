from flask import render_template, redirect, url_for, request, session
from datetime import datetime
from app.index.func import get_links_for_base, get_types_news, get_news
from app.admin.forms import NewsForm
from app.models.news import News

def start_page():
    linksall = get_links_for_base()
    typesall = get_types_news()
    arg_type = request.args.get('type_id')    
    if arg_type:
        newsall = get_news(int(arg_type))
        type_id = int(arg_type)
    else:
        newsall = get_news()
        type_id = 0
    
    if request.method == 'POST':        
        if 'changenews' in request.form:
            print(request.form)
                 
            dictform = dict(request.form)
            valuesub = dictform['changenews']
            resp = redirect(url_for('index.open_news', id=valuesub))
        
        if 'delnews' in request.form:
            dictform = dict(request.form)
            valuesub = int(dictform['delnews'])
            result = News.delete_by_id(valuesub)
            resp = redirect(url_for('index.start_page'))
        
        if 'addnews' in request.form:
            resp = redirect(url_for('index.open_news'))
            
        return resp

    return render_template('index.html', title='Техническая страница',
                           linksall=linksall, typesall=typesall,
                           newsall = newsall, type_id = type_id)
    
def open_news():
    if 'back' in request.form:
        return redirect(url_for('index.start_page'))
    
    arg_id = request.args.get('id')
    if arg_id is not None:
        news = News.get_by_id(arg_id)
        form = NewsForm(request.form or None, obj=news)
        text = news.text
        titleform = 'Изменить запись'
    else:
        form = NewsForm(request.form or None)
        titleform = 'Добавить запись'
        text = ''
    
    if request.method == 'POST' and form.validate():
        text = request.form["text"]
        d = datetime.today()
        if arg_id is not None:
            result = (News
                      .update(text=text,
                              typenews=form.typenews.data,
                              name=form.name.data,
                              changedate=d,
                              user=session.user['user_id'])
                      .where(News.id==arg_id)
                      .execute())
        else:    
            news = News(text=text,
                     typenews=form.typenews.data,
                     name=form.name.data,
                     createdate=d,
                     changedate=d,
                     user=session.user['user_id'])
            news.save()
        return redirect(url_for('index.start_page'))
    
    return render_template('newsform.html', title=titleform, 
                           form=form, text=text)
