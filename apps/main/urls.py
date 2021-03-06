from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
	url(r'^main$', views.index),
	url(r'^create_user/$', views.create_user),
	url(r'^strava_login/$', views.strava_login),
	url(r'^strava/get_stra_id/$', views.strava_get_id),
	url(r'^dashboard/$', views.dashboard),
	url(r'^logout/$', views.logout),
	url(r'^show_profile/(?P<user_id>\d+)$', views.show_profile),
	url(r'^like/(?P<liked_user_id>\d+)$', views.like),
	url(r'^match/(?P<liked_user_id>\d+)$', views.match),

]