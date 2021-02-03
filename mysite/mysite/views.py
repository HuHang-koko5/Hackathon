from django.shortcuts import render, redirect


def index(request):
    # if not request.session.get('is_login', None):
    #     # redirect to login
    #     return redirect("/user/login/")
    return render(request, 'index.html')