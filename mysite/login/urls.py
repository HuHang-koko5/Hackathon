from django.urls import path
from . import views

urlpatterns = [
    path('top/', views.hello),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout)
]