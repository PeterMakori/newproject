from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# from django contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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
class Department(models.Model):
    department = models.CharField(max_length=255)

    def __str__(self):
        return self.department

class Faculty(models.Model):
    faculty = models.CharField(max_length=255)

    def __str__(self):
        return self.faculty



class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    username = models.CharField(max_length=250, blank=False, null=False, unique=True,)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255,blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    is_student = models.BooleanField(default=False,verbose_name="student")
    is_dean = models.BooleanField(default=False, verbose_name="dean")
    is_cod =  models.BooleanField(default=False, verbose_name="cod")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null=True, blank=True)

    USERNAME_FIELD = 'username'
    objects = MyUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):

        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    #
    # @property
    # def is_active(self):
    #     return self.is_active

    # @property
    # def is_student(self):
    #     return self.is_student
    # @property
    # def is_dept_staff(self):
    #     return self.is_dept_staff





class SendFeedback(models.Model):
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    type = models.CharField(max_length=100)
    subject = models.CharField(max_length=70)
    message = models.TextField(max_length=255)
    sent_on = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return self.type + ' ' + self.subject + ' ' + self.message


# class Post(models.Model):
#     user = models.ForeignKey(User)
#     title = models.CharField(max_length=128, blank=True, default='Query')
#     notice = models.CharField(max_length=500)
#     uploadtime = models.DateField(auto_now=True)

class Notices(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    topic = models.CharField(max_length=100)
    notice = models.TextField(max_length=900)
    last_modified = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(auto_now_add=False)
