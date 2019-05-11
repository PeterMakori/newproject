from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from .forms import SignUpForm, EditProfileForm, SendFeedbackForm, StaffSignUp
from django.views.generic import CreateView
from authenticate.models import User

# Create your views here.

def Signup(request):
	return render(request, 'authenticate/divide.html')

def home(request):
	return render(request, 'authenticate/home.html', {})

def about(request):
	return render(request, 'authenticate/about.html', {})

def contact(request):
	return render(request, 'authenticate/contact.html', {})

def feedback(request):
	form = SendFeedbackForm;
	if request.method == 'POST':
		type = request.POST['type']
		subject = request.POST['subject']
		message = request.POST['message']

		form = SendFeedbackForm(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request, ('Feedback Submitted Successfully.'))
			return redirect('home')

	else:
		context = {'form':form}
		return render(request, 'authenticate/feedback.html', context)

def search(request):
	return render(request, 'authenticate/search.html', {})


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
			messages.success(request, ('Registration Number or Password Wrong. Please Try Again!'))
			return redirect('login')

	else:
		return render(request, 'authenticate/login.html', {})


# def register_user(request):
# 	if request.method == 'POST':
# 		form = SignUpForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			username = form.cleaned_data['username']
# 			password = form.cleaned_data['password1']
# 			user = authenticate(username=username,password=password)
# 			login(request,user)
# 			messages.success(request, ('Registration Successful!'))
# 			return redirect('home')
# 	else:
# 		form = SignUpForm()
# 	context = {'form':form}
# 	return render(request, 'authenticate/register.html', context)
def landing(request):
	return redirect(request, 'authenticate/landing.html', {})
def view_prof(request):
	return render(request, 'authenticate/viewprof.html', {})

def logout_user(request):
	logout(request)
	# messages.success(request, 'You have been logged out')
	return redirect('home')

def edit_profile(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('You Have Edited Your Profile.'))
			return redirect('viewprof')
	else:
		form = EditProfileForm(instance=request.user)
	context = {'form':form}
	return render(request, 'authenticate/edit_profile.html', context)

def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('You Have Changed Your Password.'))
			return redirect('home')
	else:
		form = PasswordChangeForm(user=request.user)
	context = {'form':form}
	return render(request, 'authenticate/change_password.html', context)


class StdentSignUp(CreateView):
	model = User
	form_class = SignUpForm
	template_name = 'authenticate/signup.html'

	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'student'
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return redirect('home')

class StaffSign(CreateView):
	model = User
	form_class = StaffSignUp
	template_name = 'authenticate/signup.html'

	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'staff'
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return redirect('home')
