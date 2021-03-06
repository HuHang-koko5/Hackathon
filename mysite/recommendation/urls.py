from django.urls import path
from . import views

urlpatterns = [
    path('study/<int:label>/<int:url_id>/', views.studyone, name='studyone'),
    path('study/<int:label>/', views.study, name='study'),
    path('like/', views.like, name='like'),
    path('bookmark/', views.show_bookmark),
    path('bookmark/add/', views.add_bookmark, name='add_bookmark'),
    path('bookmark/remove/', views.remove_bookmark, name='remove_bookmark'),
    # path('like/<int:prev_id>-<int:next_id>/', views.like, name='like'),
]
