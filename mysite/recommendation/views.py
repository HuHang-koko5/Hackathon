from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
import pymongo

url_type = {0: '基礎',
            1: '応用'}
label_type = {0: '式の計算',
              1: '連立方程式',
              2: '１次関数',
              3: '平行と合同',
              4: '三角形と四角形',
              5: '関数のグラフと図形',
              6: '確率'}
site_type = {0: 'Amazon',
             1: 'youtube',
             2: 'Others'}


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
        print('label :{} {}'.format(label, type(label)))
        item = col.find_one({'label': label})
        if item is None:
            print('no item!')
            message = "Sorry,we are unable to find one now, come back later!"
            messages.error(request, message)
            return render(request, 'index.html', {})
        else:
            new_url = '/reco/study/' + str(label) + '/' + str(item['url_id']) + '/'
            return redirect(new_url, {'prev': None})


def studyone(request, label, url_id, prev=None):
    if not request.session.get('is_login', None):
        message = 'please login first!'
        messages.error(request, message)
        return redirect('/index/')
    else:
        client = pymongo.MongoClient('localhost', 27017)
        db = client['Django']
        col = db['urls']
        item = col.find_one({'url_id': url_id,
                             'label': label})
        if item is None:
            message = 'Resource does not exist!'
            messages.error(request, message)
            return redirect('/index/')
        else:
            current_item = {'title': item['title'],
                            'url': item['url'],
                            'url_id': item['url_id'],
                            'type_tag': url_type[item['type']],
                            'type': item['type'],
                            'site_type': item['site_type'],
                            'label': item['label'],
                            'label_tag': label_type[item['label']],
                            'site_tag': site_type[item['site_type']],
                            }
            # pick next lists
            next_col = db['reco']
            nexts = next_col.find({'prev': url_id}).limit(5).sort('value', pymongo.DESCENDING)
            nextlist = []
            for n in nexts:
                next_url = n['next']
                next_item = col.find_one({'url_id': next_url})
                if next_item is not None:
                    nitem = next_item
                    nitem['value'] = n['value']
                    nitem['type_tag'] = url_type[nitem['type']]
                    nitem['label_tag'] = label_type[nitem['label']]
                    nitem['site_tag'] = site_type[nitem['site_type']]
                    print('next item:', nitem)
                    nextlist.append(nitem)
            if request.method == 'GET':
                prev = request.GET.get('prev')
            print('prev', prev)
            return render(request, 'study/study.html', {'items': current_item,
                                                        'nexts': nextlist,
                                                        'prev': prev})


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
        for obj in col.find({'user_id': user_name}).sort('time', pymongo.DESCENDING).limit(5):
            item = urlcol.find_one({'url_id': obj['url_id']})
            if item is not None:
                nitem = {'title': item['title'],
                         'url': item['url'],
                         'url_id': item['url_id'],
                         'type_tag': url_type[item['type']],
                         'type': item['type'],
                         'site_type': item['site_type'],
                         'label': item['label'],
                         'label_tag': label_type[item['label']],
                         'site_tag': site_type[item['site_type']],
                         'time': obj['time']
                         }
                itemlist.append(nitem)

        return render(request, 'bookmark/bookmark.html', {'items': itemlist})


def add_bookmark(request):
    if not request.session.get('is_login', None):
        message = 'please login first!'
        return redirect('/index/', message=message)
    else:
        if request.method == 'POST':
            request.session['add_from'] = request.META.get('HTTP_REFERER', '/')
            user_name = request.session['user_name']
            url_title = request.POST.get('url_title')
            url_id = int(request.POST.get('url_id'))
            url_label = int(request.POST.get('url_label'))
            prev = request.POST.get('prev_id')
            client = pymongo.MongoClient('localhost', 27017)
            print(user_name, '  ', url_id, ' ', url_title)
            db = client['Django']
            col = db['bookmark']
            reco = db['reco']
            item = col.find_one({'url_id': url_id,
                                 'title': url_title,
                                 'user_id': user_name})
            if item is None:
                print('new one')
                col.insert({'title': url_title, 'url_id': url_id, 'user_id': user_name, 'time': datetime.now()})
                message = 'Bookmark add successfully!'
                messages.success(request, message)
                if prev is not None:
                    prev = int(prev)
                    print('find pair: {} -> {}'.format(prev, url_id))
                    pair = reco.find_one({'prev': prev, 'next': url_id})
                    if pair is None:
                        reco.insert({'prev': prev,
                                     'next': url_id,
                                     'value': 1})
                        print('new')
                    else:
                        new_value = pair['value'] + 1
                        print('plus :', new_value)
                        reco.update({'prev': prev, 'next': url_id}, {'$set': {'value': new_value}})
            else:
                print('exist one ', url_label)
                message = 'This has already in your book mark!'
                messages.error(request, message)
            if prev is not None:
                return redirect('/reco/study/' + str(url_label) + '/' + str(url_id) + '/?prev=' + str(prev))
            else:
                return redirect('/reco/study/' + str(url_label) + '/' + str(url_id))
        else:
            message = 'Invalid request!'
            return redirect('/index/', message=message)


def remove_bookmark(request):
    if not request.session.get('is_login', None):
        message = 'please login first!'
        return redirect('/index/', message=message)
    else:
        if request.method == 'GET':
            url_id = request.GET.get('url_id')
            user_name = request.session['user_name']
            client = pymongo.MongoClient('localhost', 27017)
            db = client['Django']
            col = db['bookmark']
            item = col.find_one({'url_id': url_id,
                                 'user_name': user_name})
            if item is None:
                message = 'this url is not in your bookmark!'
                messages.error(request,message)
            else:
                col.remove({'url_id': url_id,
                            'user_name': user_name})
                message = 'Bookmark has been removed!'
                messages.success(request, message)
            return redirect('/reco/bookmark/')


def like(request):
    if not request.session.get('is_login', None):
        message = 'please login first!'
        return redirect('/index/', message=message)
    else:
        if request.method == 'POST':
            url_id = int(request.POST.get('url_id'))
            prev = int(request.POST.get('prev_id'))
            url_label = int(request.POST.get('url_label'))
            print('prev, next {} {}'.format(url_id, prev))
            client = pymongo.MongoClient('localhost', 27017)
            db = client['Django']
            col = db['reco']
            item = col.find_one({'prev': prev,
                                 'next': url_id})
            if item is not None:
                value = item['value']
                col.update({'prev': prev, 'next': url_id}, {'$set': {'value': value + 1}})
                message = 'Thank you for your recommendation!'
                messages.success(request, message)
                return redirect('/reco/study/' + str(url_label) + '/' + str(url_id) + '/?prev=' + str(prev) + '')
