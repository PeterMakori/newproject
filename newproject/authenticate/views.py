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
from datetime import datetime, date
import xlrd
import csv
from django.contrib.auth.hashers import make_password



# Create your views here.

def Signup(request):
	return render(request, 'authenticate/divide.html')



def homestaff(request):
	return render(request, 'authenticate/home2.html', {})

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
			if user.is_student:
				return redirect('home')
			else:
				return redirect('home2')
			
			# messages.success(request, ('You Have Been Logged In!'))
			# return redirect('home')
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
@login_required
def find_help(request):
	return render(request, 'authenticate/help.html', {})
@login_required
def search_help(request):
	return render(request, 'authenticate/staff_help.html', {})

def logout_user(request):
	logout(request)
	return redirect('login')


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
		send = SendFeedback()
		
		if form.is_valid():
			send = form.save(commit=False)
			send.sent_by = request.user
			send.facult = request.user.faculty
			send.depart = request.user.department


			where = request.POST.get('send_to')
			if where == 'yes':
				send.to_faculty = True
				send.save()
				pass
				#turn facultry to true
			else:
				send.to_department = True
				send.save()
				pass
				#turn department to true

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
	# control = False
	today = date.today()
	read = Notices.read_by.through.objects.values_list('notices').filter(user=request.user)
	# print(read)
	count_unread = Notices.objects.exclude(id__in=read).filter(due_date__gte=today).filter(posted_by__is_dean =True).filter(posted_by__faculty=request.user.faculty).order_by('-created_on').count()
	# print(count_unread)	
	notices = Notices.read_by.through.objects.filter(user=request.user).filter(notices__due_date__gte=today).filter(notices__posted_by__is_dean =True).filter(notices__posted_by__faculty=request.user.faculty).order_by('-notices__created_on')
	return render(request,'authenticate/facultynotice.html', {'notices':notices, 'count':count_unread})
	
def unread_faculty_notice(request):
	# control = False
	today = date.today()
	read = Notices.read_by.through.objects.values_list('notices').filter(user=request.user)
	notices = Notices.objects.exclude(id__in=read).filter(due_date__gte=today).filter(posted_by__is_dean =True).filter(posted_by__faculty=request.user.faculty).order_by('-created_on')
	return render(request,'authenticate/unreadnotices.html', {'notices':notices})

def faculty_notice_details(request, pk):
	notice = Notices.objects.get(pk=pk)
	notice.read_by.add(request.user)
	return render(request,'authenticate/facultynoticedetails.html', {'notice':notice})

def department_notice(request):
	today = date.today()
	read = Notices.read_by.through.objects.values_list('notices').filter(user=request.user)
	# print(read)
	count_unread = Notices.objects.exclude(id__in=read).filter(due_date__gte=today).filter(posted_by__is_cod =True).filter(posted_by__department=request.user.department).order_by('-created_on').count()
	# print(count_unread)	
	notices = Notices.read_by.through.objects.filter(user=request.user).filter(notices__due_date__gte=today).filter(notices__posted_by__is_cod =True).filter(notices__posted_by__department=request.user.department).order_by('-notices__created_on')
	return render(request,'authenticate/department_notice.html', {'notices':notices, 'count':count_unread})
	

def unread_department_notice(request):
	# control = False
	today = date.today()
	read = Notices.read_by.through.objects.values_list('notices').filter(user=request.user)
	notices = Notices.objects.exclude(id__in=read).filter(due_date__gte=today).filter(posted_by__is_cod =True).filter(posted_by__department=request.user.department).order_by('-created_on')
	return render(request,'authenticate/unreadnoticedept.html', {'notices':notices})

def department_notice_details(request, pk):
	notice = Notices.objects.get(pk=pk)
	notice.read_by.add(request.user)
	return render(request,'authenticate/department_noticed_details.html', {'notice':notice})

def view_Feedback(request):
	feedbacks = SendFeedback.objects.filter(to_faculty =True).filter(facult__faculty=request.user.faculty).order_by('-sent_on')
	return render(request,'authenticate/viewfeedback_fac.html', {'feedbacks':feedbacks} )

def Feedback_Dep(request):
	feedbacks = SendFeedback.objects.filter(to_department =True).filter(depart__department=request.user.department).order_by('-sent_on')
	return render(request,'authenticate/viewfeedback_dep.html', {'feedbacks':feedbacks} )

def Feedbackdept_Details(request, pk):
	feedback = SendFeedback.objects.get(pk=pk)
	return render(request,'authenticate/deptfeeddetails.html', {'feedback':feedback})


def Feedbackfac_Details(request,pk):
	feedback = SendFeedback.objects.get(pk=pk)
	return render(request,'authenticate/facultyfeeddetails.html', {'feedback':feedback})


def Search_Notices(request):
	notices_from = request.GET.get('from')
	notices_to = request.GET.get('to')
	if notices_from == None or notices_to ==None:
		notices_available = Notices.objects.filter(posted_by__is_dean =True).filter( posted_by__faculty=request.user.faculty).order_by('-created_on')[:3]

	else:
		notices_from = datetime.strptime(notices_from, "%Y-%m-%d").date()
		notices_to = datetime.strptime(notices_to, "%Y-%m-%d").date()
		
		notices_available = Notices.objects.filter(due_date__gte=notices_from).filter(due_date__lte=notices_to).filter(posted_by__is_dean =True).filter( posted_by__faculty=request.user.faculty).order_by('-created_on')
		
	context = {'notices_available':notices_available}
	return render(request, 'authenticate/search.html', context)

def search_notice_details(request, pk):
	search = Notices.objects.get(pk=pk)
	search.read_by.add(request.user)
	return render(request,'authenticate/search_noticed_details.html', {'search':search})

def search_dept_notice_details(request, pk):
	search = Notices.objects.get(pk=pk)
	search.read_by.add(request.user)
	return render(request,'authenticate/search_deptnoticed_details.html', {'search':search})


def Search_Dept_Notices(request):
	notices_from = request.GET.get('from')
	notices_to = request.GET.get('to')
	if notices_from == None or notices_to ==None:
		notices_available = Notices.objects.filter(posted_by__is_cod =True).filter( posted_by__department=request.user.department).order_by('-created_on')[:3]

	else:
		notices_from = datetime.strptime(notices_from, "%Y-%m-%d").date()
		notices_to = datetime.strptime(notices_to, "%Y-%m-%d").date()
		
		notices_available = Notices.objects.filter(due_date__gte=notices_from).filter(due_date__lte=notices_to).filter(posted_by__is_cod =True).filter( posted_by__department=request.user.department).order_by('-created_on')
		
	context = {'notices_available':notices_available}
	return render(request, 'authenticate/searchdept.html', context)

def Dean_Search_Notices(request):
	notices_from = request.GET.get('from')
	notices_to = request.GET.get('to')
	if notices_from == None or notices_to ==None:
		
		notices_available = Notices.objects.filter(posted_by__is_dean =True).filter( posted_by__faculty=request.user.faculty).order_by('-created_on')[:2]

	else:
		notices_from = datetime.strptime(notices_from, "%Y-%m-%d").date()
		notices_to = datetime.strptime(notices_to, "%Y-%m-%d").date()
		countprint = Notices.objects.all().count()
		notices_available = Notices.objects.filter(due_date__gte=notices_from).filter(due_date__lte=notices_to).filter(posted_by__is_dean =True).filter( posted_by__faculty=request.user.faculty).order_by('-created_on')
		
	context = {'notices_available':notices_available}
	return render(request, 'authenticate/noticereport.html', context)

def Cod_Search_Notices(request):
	notices_from = request.GET.get('from')
	notices_to = request.GET.get('to')
	if notices_from == None or notices_to ==None:
		
		notices_available = Notices.objects.filter(posted_by__is_cod =True).filter( posted_by__department=request.user.department).order_by('-created_on')[:2]

	else:
		notices_from = datetime.strptime(notices_from, "%Y-%m-%d").date()
		notices_to = datetime.strptime(notices_to, "%Y-%m-%d").date()
		# countprint = Notices.objects.all().count()
		notices_available = Notices.objects.filter(due_date__gte=notices_from).filter(due_date__lte=notices_to).filter(posted_by__is_cod =True).filter( posted_by__department=request.user.department).order_by('-created_on')
		
	context = {'notices_available':notices_available}
	return render(request, 'authenticate/deptnoticereport.html', context)


def Dean_Search_Feedback(request):
	feeds_from = request.GET.get('from')
	feeds_to = request.GET.get('to')
	if feeds_from == None or feeds_to ==None:
		feeds_available = SendFeedback.objects.filter(to_faculty =True).filter(facult__faculty=request.user.faculty).order_by('-sent_on')[:2]

	else:

		feeds_from = datetime.strptime(feeds_from, "%Y-%m-%d").date()
		feeds_to = datetime.strptime(feeds_to, "%Y-%m-%d").date()
		countprint = SendFeedback.objects.all().count()
		feeds_available = SendFeedback.objects.filter(sent_on__gte=feeds_from).filter(sent_on__lte=feeds_to).filter(to_faculty =True).filter( facult__faculty=request.user.faculty).order_by('-sent_on')
	return render(request,'authenticate/reportfeeds_fac.html', {'feeds_available':feeds_available} )


def Cod_Print_Feedback(request):
	codfeeds_from = request.GET.get('from')
	codfeeds_to = request.GET.get('to')
	if codfeeds_from == None or codfeeds_to ==None:
		codfeeds_available = SendFeedback.objects.filter(to_department =True).filter(depart__department=request.user.department).order_by('-sent_on')[:2]

	else:

		codfeeds_from = datetime.strptime(codfeeds_from, "%Y-%m-%d").date()
		codfeeds_to = datetime.strptime(codfeeds_to, "%Y-%m-%d").date()
		countprint = SendFeedback.objects.all().count()
		codfeeds_available = SendFeedback.objects.filter(sent_on__gte=codfeeds_from).filter(sent_on__lte=codfeeds_to).filter(to_department =True).filter( depart__department=request.user.department).order_by('-sent_on')
	return render(request,'authenticate/reportfeeds_department.html', {'codfeeds_available':codfeeds_available} )

def handle_uploaaded_file(request, f):
	book = xlrd.open_workbook(file_contents=f.read())
	for sheet in book.sheets():
		number_of_rows = sheet.nrows
		number_of_columns = sheet.ncols

		for row in range(1, number_of_rows):
			password = (sheet.cell(row, 1).value)
			username = (sheet.cell(row, 2).value)
			first_name = (sheet.cell(row, 3).value)
			last_name = (sheet.cell(row, 4).value)
			email = (sheet.cell(row, 5).value)
			is_student = (sheet.cell(row, 6).value)
			department_id = (sheet.cell(row, 7).value)
			faculty_id = (sheet.cell(row, 8).value)


			user = User()
			user.username = username
			user.password = make_password(password, salt = None, hasher = 'default')
			user.first_name = first_name
			user.last_name = last_name
			user.email = email
			user.is_student = True
			user.department_id = department_id
			user.faculty_id = faculty_id
			user.save()
			print(user.username)
			
			

	
			



# def UploadFile(request, f):
#     book = xlrd.open_workbook(file_contents=f.read())
#     for sheet in book.sheets():
#         number_of_rows = sheet.nrows
#         number_of_columns = sheet.ncols
#         for row in range(1, number_of_rows):
# 			# faculty_id = (sheet.)
            # password = (sheet.cell(row, 1).value)
            # username = (sheet.cell(row, 2).value)
            # first_name = (sheet.cell(row, 3).value)
            # last_name = (sheet.cell(row, 4).value)
            # email = (sheet.cell(row, 5).value)
            # is_student = (sheet.cell(row, 6).value)
            # department_id = (sheet.cell(row, 7).value)

# 			user = User()
# 			user.
			

			
def excel(request):
	if request.method == 'POST':
		print('imeingia')
		handle_uploaaded_file(request, request.FILES['add_userfile'])
		messages.success(request, ('Your file has been uploaded. Users added to system'))
		return redirect('addstudent')
	else:
		return render(request, 'authenticate/add_students.html')

def home(request):

	today = date.today()
	read = Notices.read_by.through.objects.values_list('notices').filter(user=request.user)
	print(read)
	faccount_unread = Notices.objects.exclude(id__in=read).filter(due_date__gte=today).filter(posted_by__is_dean =True).filter(posted_by__faculty=request.user.faculty).order_by('-created_on').count()
	print("faculty count"+str(faccount_unread))	
	facnotices = Notices.read_by.through.objects.filter(user=request.user).filter(notices__due_date__gte=today).filter(notices__posted_by__is_dean =True).filter(notices__posted_by__faculty=request.user.faculty)

	
	read = Notices.read_by.through.objects.values_list('notices').filter(user=request.user)
	print(read)
	deptcount_unread = Notices.objects.exclude(id__in=read).filter(due_date__gte=today).filter(posted_by__is_cod =True).filter(posted_by__department=request.user.department).order_by('-created_on').count()
	print(deptcount_unread)	
	deptnotices = Notices.read_by.through.objects.filter(user=request.user).filter(notices__due_date__gte=today).filter(notices__posted_by__is_cod =True).filter(notices__posted_by__department=request.user.department)
	return render(request,'authenticate/home.html', {'facnotices':facnotices, 'deptnotices':deptnotices,'faccount_unread':faccount_unread, 'deptcount_unread':deptcount_unread})
	



	
