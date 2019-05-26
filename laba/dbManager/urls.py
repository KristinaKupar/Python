from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.show_songs, name='show_songs'),
    url(r'^insert$', views.insert, name='insert'),
    url(r'^load_again$', views.load_from_file, name='load_again'),
    url(r'^show_singers$', views.show_singers, name='show_singers'),
    url(r'^history$', views.show_history, name='show_history'),
    url(r'^edit$', views.edit_songs, name='edit_songs'),
    url(r'^delete$', views.delete_singers, name='delete'),
    url(r'^deleteOrder$', views.delete_order, name='deleteOrder'),
    url(r'^add_order$', views.add_order, name='add_order'),
    url(r'^edit_order$', views.edit_order, name='edit_order'),
    url(r'^find$', views.find, name='find'),
    url(r'^show_in_range', views.show_singers_in_range, name='show_in_range'),
]