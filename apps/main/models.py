from __future__ import unicode_literals

from django.db import models

# Create your models here.


class User(models.Model):
	FB_id = models.IntegerField()
	STRA_id = models.CharField(max_length=255, null=True)
	STRA_accessToken = models.TextField(null=True)
	STRA_pic = models.CharField(max_length=255, null=True)
	user_friends = models.ManyToManyField('self', related_name='friends_friends')
	user_likes = models.ManyToManyField('self', related_name='liked_by')



