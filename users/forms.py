from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms

from .models import NormalUser

class UserLoginForm(AuthenticationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

	class Meta:
		model = NormalUser
		fields = ("username", "password")

class UserUpdateForm(UserChangeForm):
	username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
	first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))

	class Meta:
		model = NormalUser
		fields = ("username", "first_name", "last_name", "email")

class UserCreateForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
	first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

	class Meta:
		model = NormalUser
		fields = ("username", "first_name", "last_name", "email")
