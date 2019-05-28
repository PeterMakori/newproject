from django.urls import path
from . import views
from authenticate.views import viewFeedback,FeedbackDetails
from django.conf.urls import url


urlpatterns = [

    path('login/', views.login_user, name="login"),
    path('', views.home, name="home"),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('viewprof/', views.view_prof, name='viewprof'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password',views.change_password, name='change_password'),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('feedback/', views.feedback, name="feedback"),
    path('search/', views.search, name="search"),
    path('signup/', views.Signup, name="signup"),
    # path('signup/student', StdentSignUp.as_view(), name="signupstudent"),
    # path('signup/staff', StaffSign.as_view(), name="signupstaff"),
    path('createnotice/', views.notice, name="createnotice"),
    url(r'^faculty/notices/', views.faculty_notice, name="view_notices"),
    path('faculty/notice/<pk>/',views.faculty_notice_details, name="read_notice_details"),
    url(r'^feedbacks/', viewFeedback.as_view(), name="viewfeedback"),
    url(r'^feedback/view/(?P<pk>[0-9]+)/$', FeedbackDetails.as_view(), name="read_feedback_details"),
    url(r'^department/notices/', views.department_notice, name="department_notices"),
    path('department/notice/<pk>/',views.department_notice_details, name="read_department_notice"),



 ]
