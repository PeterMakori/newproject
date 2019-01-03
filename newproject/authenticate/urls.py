from django.conf.urls import url
from . import views


urlpatterns = [
   
    url('login/', views.login_user, name="login"),
    url('', views.home, name="home"),

 ]
