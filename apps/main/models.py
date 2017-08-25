from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserManager(models.Manager):
	
	def user_validator(self, postData):
		print postData
		try :
			user = User.objects.get(FB_id = postData['FB_id'])
			return user
		except :
			user = User.objects.create(FB_id=postData['FB_id'], first_name=postData['first_name'])
		return user

	def add_Strava(self, data) :
		if 'athlete' not in data or 'access' not in data or 'user_id' not in data :
			return False
		if 'id' not in data['athlete'] or 'profile_medium' not in data['athlete'] :
			return False
		try :
			user = User.objects.get(id = data['user_id'])
		except :
			return False
		user.STRA_id = data['athlete']['id']
		user.STRA_pic = data['athlete']['profile_medium']
		user.STRA_accessToken = data['access']
		user.save()
		return True

	def getUser(self, uid):
		try :
			user = User.objects.get(id = uid)
			return user
		except :
			return False

	def likeUser(self, user_id, liked_user_id):
		result = self.matchcheck(user_id, liked_user_id)
		if result ==0:
			Like.objects.create(user_likes=User.objects.get(id=user_id), liked_user=User.objects.get(id=liked_user_id))
		try:
			Like.objects.get(user_likes=User.objects.get(id=liked_user_id), liked_user=User.objects.get(id=user_id))
			return True		
		except:
			return False

	def matchcheck(self, user_id, liked_user_id):
		try:
			user= Like.objects.get(user_likes=User.objects.get(id=user_id),liked_user=User.objects.get(id=liked_user_id))
			try:
				liked= Like.objects.get(user_likes=User.objects.get(id=liked_user_id),liked_user=User.objects.get(id=user_id))
				return 2
			except:
				return 1
		except:
			return 0

	def matches(self, user_id):
		matches= User.objects.filter(likes__liked_user=user_id, liked_by__user_likes=user_id)
		return matches




class User(models.Model):
	first_name = models.CharField(max_length=255, null=True)
	FB_id = models.IntegerField()
	STRA_id = models.CharField(max_length=255, null=True)
	STRA_accessToken = models.TextField(null=True)
	STRA_pic = models.CharField(max_length=255, null=True)
	objects = UserManager()


class Like(models.Model):
 	user_likes = models.ForeignKey(User, related_name="likes")
 	liked_user= models.ForeignKey(User, related_name="liked_by")

