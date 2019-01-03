from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout 

# Create your views here.
def home(request):
	return render(request, 'authenticate/home.html', {})

def login_user(request):
	return render(request, 'authenticate/login.html', {})
