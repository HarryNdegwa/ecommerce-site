from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class RegisterForm(UserCreationForm):
	email=forms.EmailField(required=True)

	def clean_username(self):
		usernames=User.objects.values_list('username')
		username=self.cleaned_data['username']
		if username in usernames:
			raise forms.ValidationError("Username already exists!")
		return username



	class Meta:
		model=User
		fields=('username','email','password1','password2')
		help_texts={ # works perfectly for username and email but not password
			'username':None,
			'email':None,
		}
 
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)

			for fieldname in ['username', 'password1', 'password2']:
			    self.fields[fieldname].help_text = None



class PasswordCheckForm(forms.Form):
	password=forms.CharField(max_length=40,required=True)



class PasswordChangeForm(forms.ModelForm):
	password_confirm=forms.CharField(max_length=40,required=True)
	class Meta:
		model=User
		fields=('password',)


class ContactForm(forms.Form):
	recipient=forms.EmailField(max_length=254)

	def clean_recipient(self):
		data=self.cleaned_data['recipient']
		if 'harryndegwa4@gmail.com' not in data:
			raise forms.ValidationError("You have forgotten Harry!")
			# make sure you return data even if the error was not raised
		return data

