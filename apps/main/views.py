from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from django.utils.crypto import get_random_string
import bcrypt

def index(request):

	return render(request, "main/index.html")

# #if user not in database
# def create_user(request):

# 	#check if user is database
# 	user = User.objects.get(FB_id=request.session['FB_id'])

# 	#if not create user
# 	user = User.objects.create(FB_id=request.session['FB_id'])