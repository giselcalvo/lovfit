from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserManager(models.Manager):
	
	def user_validator(self, postData):
		error = {}
		print postData
		#check if user exist in the database
		if len(User.objects.filter(FB_id=postData['FB_id'])) == 0:
			print "creating new user: ", postData['FB_id']
			user = User.objects.create(FB_id=postData['FB_id'], first_name=postData['first_name'])
		else:
			error['user'] = "User is already in the database"
		if error:
			return error	
		return user

	def add_Strava(request, data) :
		if 'athlete' not in data or 'access' not in data or 'user_id' not in data :
			return False
		if 'id' not in data['athlete'] or 'profile_medium' not in data['athlete'] :
			return False
		try :
			user = User.objects.get(FB_id = data['user_id'])
		except :
			print "works haha"
			return False
		user.STRA_id = data['athlete']['id']
		user.STRA_pic = data['athlete']['profile_medium']
		user.STRA_accessToken = data['access']
		return True
	


class User(models.Model):
	first_name = models.CharField(max_length=255, null=True)
	FB_id = models.IntegerField()
	STRA_id = models.CharField(max_length=255, null=True)
	STRA_accessToken = models.TextField(null=True)
	STRA_pic = models.CharField(max_length=255, null=True)
	user_friends = models.ManyToManyField('self', related_name='friends_friends')
	user_likes = models.ManyToManyField('self', related_name='liked_by')
	objects = UserManager()
