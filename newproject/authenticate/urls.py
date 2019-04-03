from django.urls import path
from . import views


urlpatterns = [

    path('login/', views.login_user, name="login"),
    path('', views.home, name="home"),
    path('register/', views.register_user, name='register'),
    path('landing/', views.landing, name='landing'),
    path('logout/', views.logout_user, name='logout'),
    path('viewprof/', views.view_prof, name='viewprof'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password',views.change_password, name='change_password'),


 ]
