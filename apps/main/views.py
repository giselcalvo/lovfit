from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
import bcrypt, json, base64
from models import User
import requests

def index(request):

	return render(request, "main/index.html")

@csrf_exempt
def create_user(request):
	print "I am in create user"
	data = json.loads(request.POST['content'])
	request.session['FB_id'] = data['FB_id']
	result = User.objects.user_validator(data)

	if type(result) == dict:
		errors = result
		print errors
		return redirect('/')
	else:
		request.session['id'] = result.id
		request.session['first_name'] = result.first_name
		print "added user with no errors, user ID: ",request.session['id'], user	

	return redirect ('/')

def strava_login(request) :
	if not 'id' in request.session :
		return redirect('/')
	url = "https://www.strava.com/oauth/authorize?client_id=19767&response_type=code&redirect_uri=http://localhost:8000/strava/get_stra_id/&scope=view_private&state=mystate&approval_prompt=force"
	return redirect(url)

def strava_get_id(request) :
	if not 'id' in request.session :
		return redirect('/')
	url = "https://www.strava.com/oauth/token?client_id=19767&client_secret=920f2aa88fa3b85edf15ff64142d8d09dbc26027&code="
	url += request.GET['code']
	response = requests.post(url).json()
	headers = {'Authorization': "Bearer " + response['access_token']}
	url = "https://www.strava.com/api/v3/athletes/"
	url += str(response['athlete']['id'])
	athlete = requests.get(url, headers=headers).json()
	content = {
		'athlete': athlete,
		'access': encodeToken(response['access_token'], 5),
		'user_id': request.session['id']
	}
	result = User.objects.add_Strava(content)
	print type(result)
	print result
	if result :
		return HttpResponse('Success!')
	return HttpResponse('Loser!')

def encodeToken(access_token, n) :
	for i in range(n + 1) :
		access_token = base64.b64encode(access_token)
	return access_token + str(n)

def decodeToken(hashed_token) :
	n = hashed_token[-1]
	hashed_token = hashed_token[:-1]
	for i in range(int(n) + 1) :
		hashed_token = base64.b64decode(hashed_token)
	return hashed_token

# def getActivities(request) :
# 	url = "https://www.strava.com/api/v3/athlete/activities"
# 	headers = {'Authorization': "Bearer "+request.session['access_token']}
# 	data = {'per_page': 10}
# 	response = requests.get(url, headers=headers, params=data)
# 	response = response.json()
# 	print response
# 	return render(request, 'login/activities.html', {'content': response})

