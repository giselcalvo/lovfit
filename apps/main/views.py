from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
import bcrypt, json
from models import User

def index(request):

	return render(request, "main/index.html")

#if user not in database
@csrf_exempt
def create_user(request):
	print "I am in create user"
	data = json.loads(request.POST['content'])
	print data['FB_id']
	print data['friends'][0]['name']	
	request.session['id'] = data['FB_id']

	result = User.objects.user_validator(data)

	print "session: ", request.session['FB_id']

	#print "sessions:", request.session['FB_id']


	#Check if user exist in database


	# for key, item in request.POST.iteritems() :
	# 	if key == 'FB_id' :
	# 		print 'yay'
	# 	print key, item

	#print request.POST['FB_id']
	# print request
	# #check if user is database
	# user = User.objects.get(FB_id=request.session['FB_id'])

	# #if not create user
	# user = User.objects.create(FB_id=request.session['FB_id'])

	return render(request, "main/index.html")