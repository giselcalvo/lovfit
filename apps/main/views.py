from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime, strptime
from django.views.decorators.csrf import csrf_exempt
import json, base64
from models import User
import requests

def index(request):
	print 'index'
	if 'id' in request.session :
		return redirect('/dashboard/')
	return render(request, "main/index.html")

@csrf_exempt
def create_user(request):
	print 'create user'
	data = json.loads(request.POST['content'])
	result = User.objects.user_validator(data)
	request.session['id'] = result.id
	request.session['first_name'] = result.first_name
	return HttpResponse("success")

def strava_login(request) :
	print "strava_login"
	if not 'id' in request.session :
		return redirect('/')
	try :
		user = User.objects.get(id = request.session['id'])
		if user.STRA_accessToken :
			return redirect('/dashboard/')
	except :
		pass
	url = "https://www.strava.com/oauth/authorize?client_id=19767&response_type=code&redirect_uri=http://localhost:8000/strava/get_stra_id&scope=view_private&state=mystate&approval_prompt=force"
	return redirect(url)

def strava_get_id(request) :
	print 'strava_get_id'
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
	if result :
		return redirect('/dashboard/')
	return redirect('/')

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

def dashboard(request) :
	print 'dashboard'
	if not 'id' in request.session :
		return redirect('/')
	user = User.objects.getUser(request.session['id'])
	if not user :
		return ('/logout/')
	url = "https://www.strava.com/api/v3/athlete"
	headers = {'Authorization': "Bearer " + decodeToken(user.STRA_accessToken)}
	athlete = requests.get(url, headers=headers).json()
	allUsers = User.objects.all()
	allActs = []
	for item in allUsers :
		if item == user :
			continue
		url = "https://www.strava.com/api/v3/athlete/activities"
		headers = {'Authorization': "Bearer " + decodeToken(item.STRA_accessToken)}
		if len(allUsers) >= 10 :
			data = {'per_page': 1}
		else :
			data = {'per_page': 10 / (len(allUsers) - 1) + 1}
		response = requests.get(url, headers=headers, params=data).json()
		allActs += response
	sortByTime(allActs)
	allActs = allActs[:10]
	for item in allActs :
		thisUser = allUsers.get(STRA_id = item['athlete']['id'])
		item['athlete']['first_name'] = thisUser.first_name
		item['athlete']['uid'] = thisUser.id
		item['athlete']['profile'] = thisUser.STRA_pic
		item['distance'] = round(float(item['distance']) / 5280, 2)
		item['start_date_local'] = strftime("%c", strptime(item['start_date_local'], "%Y-%m-%dT%H:%M:%SZ"))
		item['photos'] = []
		if int(item['total_photo_count']) :
			url = "https://www.strava.com/api/v3/activities/"
			url += str(item['id'])
			url += "/photos?photo_sources=true"
			response = requests.get(url, headers=headers).json()
			for stuff in response :
				item['photos'].append(stuff['urls']['0'])
		item['elapsed_time'] = convertTime(item['elapsed_time'])
	content = {
		'athlete': athlete,
		'activities': allActs
	}
	return render(request, 'main/dashboard.html', content)

def convertTime(seconds) :
	rs = str(int(seconds) / 3600) + ':'
	seconds = int(seconds) % 3600
	rs += str(seconds / 60) + ':'
	seconds = seconds % 60
	rs += str(seconds)
	return rs

def sortByTime(acts) :
	sortHelper(acts, 0, len(acts) - 1)
	return

def sortHelper(acts, start, end) :
	if start >= end :
		return

	left = start
	right = end
	middle = acts[(start + end) / 2]['start_date_local']

	while left <= right :
		while left <= right and acts[left]['start_date_local'] > middle :
			left += 1
		while left <= right and acts[right]['start_date_local'] < middle :
			right -= 1
		if left <= right :
			temp = acts[left]
			acts[left] = acts[right]
			acts[right] = temp
			left += 1
			right -= 1

	sortHelper(acts, start, right)
	sortHelper(acts, left, end)

def logout(request):
	print 'logout'
	request.session.clear()
	return redirect('/')

def show_profile(request, user_id):
	if not 'id' in request.session :
		return redirect('/')

	otherUser=True
	if str(request.session['id'])==str(user_id):
		otherUser=False


	print "show_profile"
	user = User.objects.get(id=user_id)

	headers = {'Authorization': "Bearer " + decodeToken(user.STRA_accessToken)}
	url = "https://www.strava.com/api/v3/athlete"
	athlete = requests.get(url, headers=headers).json()
	athlete['updated_at'] = strftime("%c", strptime(athlete['updated_at'], "%Y-%m-%dT%H:%M:%SZ"))
	headers = {'Authorization': "Bearer " + decodeToken(user.STRA_accessToken)}
	url = "https://www.strava.com/api/v3/athlete/activities/"
	data = {'per_page': 10}
	activities = requests.get(url, headers=headers, params=data).json()
	for activity in activities :
		activity['start_date_local'] = strftime("%c", strptime(activity['start_date_local'], "%Y-%m-%dT%H:%M:%SZ"))
		activity['elapsed_time'] = convertTime(activity['elapsed_time'])
		activity['distance'] = round(float(activity['distance']) / 5280, 2)
		activity['photos'] = []
		if int(activity['total_photo_count']) :
			url = "https://www.strava.com/api/v3/activities/"
			url += str(activity['id'])
			url += "/photos?photo_sources=true"
			response = requests.get(url, headers=headers).json()
			for stuff in response :
				activity['photos'].append(stuff['urls']['0'])

	match = User.objects.matchcheck(request.session['id'], user_id)
	like=False

	if match==1:
		like=True
	content = {
		'athlete': athlete,
		'activities': activities,
		'match':match,
		'id':user_id,
		'like':like,
		'otherUser':otherUser
	}
	return render(request, 'main/profile.html', content)

def like(request, liked_user_id):
	print "like"
	liked_user = User.objects.get(id=liked_user_id)
	user = User.objects.likeUser(request.session['id'], liked_user.id)
	liked_user = User.objects.get(id=liked_user_id)
	match = User.objects.likeUser(request.session['id'], liked_user_id)
	if match :
		return redirect('/match/'+str(liked_user_id))
	return redirect('/show_profile/'+str(liked_user.id))


def match(request, liked_user_id):
	result = User.objects.matchcheck(request.session['id'], liked_user_id)
	if result <2:
		return redirect('/show_profile/'+str(liked_user_id))
	content={
		'user':User.objects.get(id=request.session['id']),
		'match':User.objects.get(id=liked_user_id),
	}
	return render(request, "main/match.html", content)


