from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from authenticate.models import User
from django import forms
from .models import SendFeedback,Notices
from django.forms import ModelForm,Textarea

class EditProfileForm(UserChangeForm):
    email = forms.EmailField(label="", help_text = '', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control mt-5', 'placeholder':'Last Name'}))
    faculty = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Faculty'}))
    department = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Department'}))
    password = forms.CharField(label="", widget=forms.TextInput(attrs={'type':'hidden'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password',)


    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ""
        self.fields['username'].help_text = '<span class = "form-text text-muted"><small> Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small> </span>'




class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    faculty = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Faculty'}))
    department = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Department'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'faculty', 'department', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Registration No.'
        self.fields['username'].label = ""
        self.fields['username'].help_text = '<span class = "form-text text-muted"><small> 15 characters or fewer with Letters, digits and  _ only.</small> </span>'


        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ""
        self.fields['password1'].help_text = '<ul class = "form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'


        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ""
        self.fields['password2'].help_text = '<span class = "form-text text-muted"> <small> Enter the same password as before, for verification.</small> </span>'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
        return user

class StaffSignUp(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super(StaffSignUp, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ""
        self.fields['username'].help_text = '<span class = "form-text text-muted"><small> Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small> </span>'


        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ""
        self.fields['password1'].help_text = '<ul class = "form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'


        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ""
        self.fields['password2'].help_text = '<span class = "form-text text-muted"> <small> Enter the same password as before, for verification.</small> </span>'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
        return user


CHOICES = [('yes','Faculty'), ('no','Department')] 
class SendFeedbackForm(forms.ModelForm):
    send_to = forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect())
    class Meta:
        model = SendFeedback
        fields = ('type', 'subject', 'message')
        widgets = {
            'message': Textarea(attrs={'class':'form-control','cols':4, 'rows':5}),
        }

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notices
        fields = ('topic','notice','due_date',)
        widgets = {
            'notice': Textarea(attrs={'class':'form-control','cols':4, 'rows':5}),
        }
