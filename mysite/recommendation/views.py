from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
import pymongo

url_type = {'0': '基礎',
            '1': '応用'}
label_type = {'0': '式の計算',
              '1': '連立方程式',
              '2': '１次関数',
              '3': '平行と合同',
              '4': '三角形と四角形',
              '5': '関数のグラフと図形',
              '6': '確率'}
site_type = {'0': 'Amazon',
             '1': 'youtube',
             '2': 'Others'}


# Create your views here.

def study(request, label):
    if not request.session.get('is_login', None):
        message = 'please login first!'
        messages.error(request, message)
        return redirect('/index/')
    else:
        client = pymongo.MongoClient('localhost', 27017)
        db = client['Django']
        col = db['urls']
        item = col.find_one({'label': str(label)})
        if item is None:
            print('no item!')
            message = "Sorry,we are unable to find one now, come back later!"
            messages.error(request, message)
            return render(request, 'index.html', {})
        else:
            new_url = '/reco/study/' + str(label) + '/' + str(item['url_id']) + '/'
            return redirect(new_url)


def studyone(request, label, url_id):
    if not request.session.get('is_login', None):
        message = 'please login first!'
        messages.error(request, message)
        return redirect('/index/')
    else:
        client = pymongo.MongoClient('localhost', 27017)
        db = client['Django']
        col = db['urls']
        item = col.find_one({'url_id': str(url_id),
                             'label': str(label)})
        if item is None:
            message = 'Resource does not exist!'
            messages.error(request, message)
            return redirect('/index/')
        else:
            nitem = {'title': item['title'],
                     'url': item['url'],
                     'url_id': item['url_id'],
                     'type_tag': url_type[item['type']],
                     'type': item['type'],
                     'label_tag': label_type[item['label']],
                     'label': item['label'],
                     'site_type': site_type[item['site_type']]}
            return render(request, 'study/study.html', {'items': [nitem]})


def show_bookmark(request):
    if not request.session.get('is_login', None):
        message = 'please login first!'
        return redirect('/index/', message=message)
    else:
        user_name = request.session['user_name']
        client = pymongo.MongoClient('localhost', 27017)
        db = client['Django']
        col = db['bookmark']
        urlcol = db['urls']
        itemlist = []
        for item in col.find({'user_id': user_name}).sort('time', pymongo.DESCENDING).limit(5):
            obj = urlcol.find_one({'url_id': item['url_id']})
            if obj is not None:
                nitem = {'title': item['title'],
                         'url_id': item['url_id'],
                         'url': obj['url'],
                         'time': item['time'],
                         'label': obj['label'],
                         'label_tag': label_type[obj['label']]
                         }
                itemlist.append(nitem)
        return render(request, 'bookmark/bookmark.html', {'items': itemlist})


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
                messages.success(request, message)
            else:
                message = 'This has already in your book mark!'
                messages.error(request, message)
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
