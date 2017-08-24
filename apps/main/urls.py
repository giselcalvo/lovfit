from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
	url(r'^main$', views.index),
	url(r'^create_user/$', views.create_user)

]