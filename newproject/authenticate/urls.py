from django.urls import path
from . import views
# from authenticate.views import view_Feedback,Feedback_Details
from django.conf.urls import url


urlpatterns = [

    path('login/', views.login_user, name="login"),
    path('', views.home, name="home"),
    path('register/', views.register_user, name='register'),
    path('help/', views.find_help, name='studenthelp'),
    path('staff/help/', views.search_help, name='staffhelp'),
    path('logout/', views.logout_user, name='logout'),
    path('viewprof/', views.view_prof, name='viewprof'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password',views.change_password, name='change_password'),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('feedback/', views.feedback, name="feedback"),
    path('signup/', views.Signup, name="signup"),
    # path('signup/student', StdentSignUp.as_view(), name="signupstudent"),
    # path('signup/staff', StaffSign.as_view(), name="signupstaff"),
    path('createnotice/', views.notice, name="createnotice"),
    url(r'^faculty/notices/', views.faculty_notice, name="view_notices"),
    url(r'^faculty/unread/notices/', views.unread_faculty_notice, name="unread_view_notices"),
    path('faculty/notice/<pk>/',views.faculty_notice_details, name="read_notice_details"),
    url(r'^feedbacks/faculty', views.view_Feedback, name="viewfeedbackfac"),
    path('feedback/faculty/details/<pk>/', views.Feedbackfac_Details, name="read_feedback_details"),
    url(r'^feedbacks/department', views.Feedback_Dep, name="viewfeedbackdep"),    
    path('feedback/department/details/<pk>/', views.Feedbackdept_Details, name="read_feed_details"),
    url(r'^department/notices/', views.department_notice, name="department_notices"),
    url(r'^department/unread/notices/', views.unread_department_notice, name="unread_department_notices"),
    path('department/notice/<pk>/',views.department_notice_details, name="read_department_notice"),
    url(r'^search/notices/', views.Search_Notices, name="search"),
     url(r'^reports/notices/', views.Dean_Search_Notices, name="reports"),
    path('search/notice/<pk>/',views.search_notice_details, name="read_search_details"),
    path('reports/notices/', views.Dean_Print, name="printreports"),
    



 ]
