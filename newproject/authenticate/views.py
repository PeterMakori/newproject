from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from .forms import SignUpForm, EditProfileForm, SendFeedbackForm, StaffSignUp,NoticeForm
from django.contrib.auth.decorators import login_required
from authenticate.decorators import staff_required,student_required
from django.views.generic import CreateView,TemplateView,ListView,DetailView
from authenticate.models import User,Notices,SendFeedback
from django.utils.decorators import method_decorator
from datetime import date


# Create your views here.

def Signup(request):
	return render(request, 'authenticate/divide.html')

def home(request):
	return render(request, 'authenticate/home.html', {})

def about(request):
	return render(request, 'authenticate/about.html', {})

def contact(request):
	return render(request, 'authenticate/contact.html', {})
#
# def admin_notice(request):
# 	return render(request, 'authenticate/adminnotice.html', {})
#
# def faculty_notice(request):
# 	return render(request, 'authenticate/facultynotice.html', {})
#
# # def department_notice(request):
# # 	return render(request, 'authenticate/departmentnotice.html', {})

# def accommodation_notice(request):
# 	return render(request, 'authenticate/accommodationnotice.html', {})

@login_required
@student_required
def search(request):
	return render(request, 'authenticate/search.html', {})


def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			# messages.success(request, ('You Have Been Logged In!'))
			return redirect('home')
		else:
			messages.success(request, ('Username or Password Wrong. Please Try Again!'))
			return redirect('login')

	else:
		return render(request, 'authenticate/login.html', {})


def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username,password=password)
			login(request,user)
			messages.success(request, ('Registration Successful!'))
			return redirect('home')
	else:
		form = SignUpForm()
	context = {'form':form}
	return render(request, 'authenticate/register.html', context)

@login_required
def view_prof(request):
	return render(request, 'authenticate/viewprof.html', {})

def logout_user(request):
	logout(request)
	return redirect('home')


@login_required
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

@login_required
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('You Have Changed Your Password.'))
			return redirect('change_password')
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
		# login(self.request, user) no need to login directly
		 # messages.success(('Registration Successful!'))
		return redirect('login')

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


@login_required
def notice(request):
	form = NoticeForm(request.POST or None)
	if request.method == 'POST':
		form = NoticeForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.posted_by = request.user
			post.save()
			messages.success(request,('Your Notice has been posted'))
			return redirect('createnotice')
	else:
		form = NoticeForm()
	context = {'form': form}
	return render(request, 'authenticate/createnotice.html', context)

@login_required
@student_required
def feedback(request):
	form = SendFeedbackForm(request.POST or None)
	if request.method == 'POST':
		form = SendFeedbackForm(request.POST)
		if form.is_valid():
			send = form.save(commit=False)
			send.sent_by = request.user
			send.save()
			messages.success(request,('Feedback Submitted Successfully'))
			return redirect('feedback')
		else:
			form = SendFeedbackForm()
	context = {'form': form}
	return render(request, 'authenticate/feedback.html', context)


# @method_decorator([login_required], name='dispatch')
# class ViewNotice(ListView):
# 	template_name = 'authenticate/facultynotice.html'
# 	context_object_name = 'notices'
# 	def get_queryset(self):
# 		today = date.today()
# 		return Notices.objects.filter(due_date__gte=today).order_by('-created_on')

# @method_decorator([login_required], name='dispatch')
# class NoticeDetails(DetailView):
# 	model = Notices
# 	print(Notices)
# 	template_name = 'authenticate/noticedetails.html'

def faculty_notice(request):
	today = date.today()
	notices = Notices.objects.filter(due_date__gte=today).filter(posted_by__is_dean =True).order_by('-created_on')
	return render(request,'authenticate/facultynotice.html', {'notices':notices} )

def faculty_notice_details(request, pk):
	notice = Notices.objects.get(pk=pk)
	return render(request,'authenticate/facultynoticedetails.html', {'notice':notice})

def department_notice(request):
	today = date.today()
	notices = Notices.objects.filter(due_date__gte=today).filter(posted_by__is_cod =True).order_by('-created_on')
	return render(request,'authenticate/department_notice.html', {'notices':notices} )

def department_notice_details(request, pk):
	notice = Notices.objects.get(pk=pk)
	return render(request,'authenticate/department_noticed_details.html', {'notice':notice})

def view_Feedback(request):
	feedbacks = SendFeedback.objects.filter().order_by('-sent_on')
	return render(request,'authenticate/viewfeedback.html', {'feedbacks':feedbacks} )

def Feedback_Details(request, pk):
	feedback = SendFeedback.objects.get(pk=pk)
	return render(request,'authenticate/facultyfeeddetails.html', {'feedback':feedback})
