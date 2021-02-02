from django.shortcuts import render, redirect
from datetime import datetime
import pymongo


# Create your views here.

def study(request, label):
    if not request.session.get('is_login', None):
        message = 'please login first!'
        return redirect('/index/', message=message)
    else:
        client = pymongo.MongoClient('localhost', 27017)
        db = client['Django']
        col = db['urls']
        item = col.find_one({'label': label})
        new_url = '/study/'+str(label)+'/'+str(item['ur;_id'])+'/'
        redirect(new_url)


def studyone(request, label, url_id):
    if not request.session.get('is_login', None):
        message = 'please login first!'
        return redirect('/index/', message=message)
    else:
        client = pymongo.MongoClient('localhost', 27017)
        db = client['Django']
        col = db['urls']
        item = col.find_one({'url_id': url_id,
                            'label': label})
        if item is None:
            message = 'Resource does not exist!'
            redirect('/index/', message=message)
        else:
            render('study/study.html', {'url': item['url'],
                                        'type': item['type'],
                                        'label': item['label'],
                                        'site_type': item['site_type'],
                                        'title': item['title']
                                        })


def add_bookmark(request, url_id):
    if not request.session.get('is_login', None):
        message = 'please login first!'
        return redirect('/index/', message=message)
    else:
        if request.method == 'GET':
            request.session['add_from'] = request.META.get('HTTP_REFERER', '/')
            user_name = request.session['user_name']
            client = pymongo.MongoClient('localhost', 27017)
            db = client['Django']
            col = db['bookmarks']
            item = col.find_one({'url_id': url_id,
                                 'user_name': user_name})
            if item is None:
                col.insert({'url_id': url_id, 'user_name': user_name, 'time': datetime.now()})
                message = 'Bookmark add successfully!'
            else:
                message = 'This has already in your book mark!'
            redirect('/study/' + url_id + '/', message=message)


def remove_bookmark(request, url_id):
    if not request.session.get('is_login', None):
        message = 'please login first!'
        return redirect('/index/', message=message)
    else:
        if request.method == 'GET':
            request.session['add_from'] = request.META.get('HTTP_REFERER', '/')
            user_name = request.session['user_name']
            client = pymongo.MongoClient('localhost', 27017)
            db = client['Django']
            col = db['bookmarks']
            item = col.find_one({'url_id': url_id,
                                 'user_name': user_name})
            if item is None:
                message = 'this url is not in your bookmark!'
            else:
                col.remove({'url_id': url_id,
                            'user_name': user_name})
                message = 'Bookmark has been removed!'
            redirect('/study/' + url_id + '/', message=message)

# def like(request,prev_id,next_id):
