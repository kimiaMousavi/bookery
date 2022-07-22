"""Defines URL patterns for users"""
from django.conf.urls import url
from . import views

urlpatterns = [
    # register
    url('register', views.register, name='register'),
]
