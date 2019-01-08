from django.conf.urls import url
from . import views


urlpatterns = [
   
    url('login/', views.login_user, name="login"),
    url('', views.home, name="home"),
    url('register/', views.register_user, name='register'),
    url('landing/', views.landing, name='landing'),
    url('logout/', views.logout_user, name='logout'),

 ] 
