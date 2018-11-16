from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^get_all_rooms/$', views.get_all_rooms, name='get_all_rooms'),
	url(r'^get_available_rooms/$', views.get_available_rooms, name='get_available_rooms'),
	url(r'^make_booking/$', views.make_booking, name='make_booking'),
]
