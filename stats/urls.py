from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin', views.sign_in, name='signin'),
    path('callback', views.callback, name='callback'),
    path('remove_token', views.remove_token, name='remove_token'),
    path('signout', views.sign_out, name='signout'),
    path('league_info', views.show_league_info, name='show_league_info'),
]
