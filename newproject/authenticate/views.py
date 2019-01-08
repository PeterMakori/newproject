from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages

# Create your views here.
def home(request):
	return render(request, 'authenticate/home.html', {})

def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ('You Have Been Logged In!'))
			return redirect('home')
		else:
			messages.success(request, ('Error Logging In. Please Try Again!'))
			return redirect('login')

	else:
		return render(request, 'authenticate/login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, ('About to logout'))
	return redirect('home')


def register_user(request):
	return render(request, 'authenticate/register.html', {})
def landing(request):
	return redirect(request, 'authenticate/landing.html', {})
