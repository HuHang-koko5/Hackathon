from django.shortcuts import render, redirect
from . import forms, models
import pymongo


def register(request):
    if request.method == "POST":
        register_form = forms.RegisterUserForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            pwd1 = register_form.cleaned_data['password1']
            pwd2 = register_form.cleaned_data['password2']
            user_sex = register_form.cleaned_data['sex']
            if pwd1 == pwd2:
                client = pymongo.MongoClient('localhost', 27017)
                db = client['Django']
                col = db['users']
                db_user = col.find_one({'name': username})
                if db_user is not None:
                    message = "Username already exists！"
                    return render(request, 'login/register.html', {'register_form': register_form, 'message': message})
                else:
                    try:
                        new_user = {'name': username, 'password': pwd1, 'gander': user_sex}
                        col.insert(new_user)
                        return redirect('/index/')
                    except Exception as e:
                        return render(request, 'login/register.html',
                                      {'register_form': register_form, 'message': str(e)})
            else:
                message = 'passwords are inconsistent'
                return render(request, 'login/register.html', {'message': message})
        else:
            message = '用户名不能为空'
            return render(request, 'login/register.html', {'message': message})
    register_form = forms.RegisterUserForm()
    return render(request, 'login/register.html', {'register_form': register_form})


def login(request):
    if request.method == "POST":
        login_form = forms.LoginUserForm(request.POST)
        message = ""
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            if username is not None:
                client = pymongo.MongoClient('localhost', 27017)
                db = client['Django']
                col = db['users']
                db_user = col.find_one({'name': username})
                if db_user is None:
                    message = 'User does not exist!'
                elif db_user['password'] == password:
                    request.session['is_login'] = True
                    request.session['user_name'] = username
                    return redirect("/index/")
                else:
                    message = 'Invalid password'
            else:
                message = 'Form error'
        return render(request, 'login/login.html', locals())
    login_form = forms.LoginUserForm()
    return render(request, 'login/login.html', {'login_form': login_form})


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    return render(request, "index.html", {'message': 'Logged out！'})
