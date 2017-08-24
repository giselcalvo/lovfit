from __future__ import unicode_literals

from django.db import models

# Create your models here.
class	UserManager(models.Manager) :
	def add_Strava(request, data) :
		if 'athlete' not in data or 'access' not in data or 'user_id' not in data :
			return False
		if 'id' not in data['athlete'] or 'profile_medium' not in data['athlete'] :
			return False
		try :
			user = User.object.get(id = data['id'])
		except :
			return False
		user.STRA_id = data['athlete']['id']
		user.STRA_pic = data['athlete']['profile_medium']
		user.STRA_accessToken = data['access']
		return True

class	User(models.Model) :
	FB_id = models.IntegerField()
	STRA_id = models.CharField(max_length=255, null=True)
	STRA_accessToken = models.TextField(null=True)
	STRA_pic = models.CharField(max_length=255, null=True)
	user_friends = models.ManyToManyField('self', related_name='friends_friends')
	user_likes = models.ManyToManyField('self', related_name='liked_by')
