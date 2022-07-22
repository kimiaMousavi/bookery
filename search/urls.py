from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('main', views.main_page, name='main'),
    path('normalsearch', views.normal_search, name='normal_search'),
    path('advancedsearch', views.advanced_search, name='advanced_search'),
    path('bookmark', views.bookmark_history, name='bookmark_history'),
    path('add_bookmark', views.add_bookmark, name='add_bookmark'),
    path('bookmark_history', views.bookmark_history, name='bookmark_history'),
    path('comingSoon', views.comingSoon, name='coming_Soon'),

]

app_name = 'search'
