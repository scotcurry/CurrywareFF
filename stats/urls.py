from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin', views.sign_in, name='signin'),
    path('callback', views.callback, name='callback'),
]
