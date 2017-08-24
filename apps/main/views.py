from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
import bcrypt, json
from models import User

def index(request):

	return render(request, "main/index.html")

@csrf_exempt
def create_user(request):
	print "I am in create user"
	data = json.loads(request.POST['content'])
	request.session['id'] = data['FB_id']
	result = User.objects.user_validator(data)

	print "session: ", request.session['FB_id']


	return redirect ('/strava_login')