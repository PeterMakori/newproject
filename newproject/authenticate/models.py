from django.db import models
from django.contrib.auth.models import AbstractUser
# from django contrib.auth.forms import UserCreationForm
# from django contrib.auth.models import User
# from django import forms
#
# Create your models here.
#
# class MoreSignUp(UserCreationForm):
#
#     faculty = forms.CharField(max_length=100)
#     department = forms.CharField(max_length=100)
#
#     class Meta:
#         model = User
#         fields = ('username','first_name','last_name','email','faculty','department','password1','password2', )
#

class User(AbstractUser):
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)




class SendFeedback(models.Model):
    type = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    message = models.CharField(max_length=6000)

    def __str__(self):
        return self.type + ' ' + self.subject + ' ' + self.message
