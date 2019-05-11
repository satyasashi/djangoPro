from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

class CustomUserCreationForm(forms.Form):
	username = forms.CharField(label="Enter Username", min_length=4, max_length=150)
	email = forms.EmailField(label="Enter Your Email")
	password1 = forms.CharField(label="Enter Password", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

	# Custom Validation
	def clean_username(self):
		# Take username value from form's cleaned_data
		# and check if that username already exist.
		# If YES, Raise ValidationError.
		username= self.cleaned_data['username'].lower()
		r = User.objects.filter(username=username)
		if r.count():
			# if username already exists.
			raise ValidationError("Username already exists.")
		return username

	def clean_email(self):
		# Take username value from form's cleaned_data
		# and check if that username already exist.
		# If YES, Raise ValidationError.
		email = self.cleaned_data['email'].lower()
		r = User.objects.filter(email=email)
		if r.count():
			# if email already exists.
			raise ValidationError("Email already exists")
		return email


	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		# If Passwords don't match
		if password1 and password2 and password1 != password2:
			raise ValidationError("Passwords don't match")

	def save(self, commit=True):
		user = User.objects.create_user(
			self.cleaned_data['username'],
			self.cleaned_data['email'],
			self.cleaned_data['password1']
			)
		return user