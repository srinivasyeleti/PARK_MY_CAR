from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Account

from django.contrib.auth import authenticate

class UserRegistrationForm(UserCreationForm) :
	email = forms.CharField(max_length=30, widget = forms.EmailInput(attrs={'placeholder': 'email'}))
	username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'username'}))
	password1 = forms.CharField(max_length=30, widget = forms.PasswordInput(attrs={'placeholder': 'Password'}))
	password2 = forms.CharField(max_length=30, widget = forms.PasswordInput(attrs={'placeholder': 'confirm password'}))
	class Meta :
		model = Account
		fields = ('email', 'username', 'password1', 'password2')
		# "fields" is used to order the fields on the document,

class UserAuthenticationForm(forms.ModelForm) :
	# gonna have these fields,
	email		= forms.EmailField(label = 'Email', widget = forms.EmailInput(attrs={'placeholder': 'email'}))
	password	= forms.CharField(label = 'Password', widget = forms.PasswordInput(attrs={'placeholder': 'password'}))

	class Meta :
		model = Account		# tells dj what model does the form look like,
		fields = ('email', 'password')

	def clean(self) :
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']

			# if the user has given wromg credentials,

			# if not authenticate(email = 'email', password = 'password') :
			if not authenticate(email = email, password = password) :
				raise forms.ValidationError('Invalid login')


class AccountUpdationForm(forms.ModelForm) :
	
	class Meta :		# i kept meta instead of Meta and got error ValueError at /profile/ ModelForm has no model class specified 
		model = Account
		fields = ('email', 'username')

	def clean_email(self) :		# trying to get email
		if self.is_valid() :
			email = self.cleaned_data['email']

			# making sure that the new email is not in use,
			try :
				account = Account.objects.exclude(pk = self.instance.pk).get(email = email)
			except :
				return email
			
			raise forms.ValidationError('email "%s" is already in use...' %account.email)


	def clean_username(self) :		# trying to get username
		if self.is_valid() :
			username = self.cleaned_data['username']

			# making sure that the new username is not in use,
			try :
				account = Account.objects.exclude(pk = self.instance.pk).get(username = username)
			except :
				return username
			
			raise forms.ValidationError('username "%s" is already in use...' %account.username)