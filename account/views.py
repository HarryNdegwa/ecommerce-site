from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login,authenticate

from .forms import RegisterForm,PasswordCheckForm
from shop.models import Notification

# @sensitive_post_parameters
def register(request):
	if request.method=="POST":
		form=RegisterForm(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			password=form.cleaned_data['password1']
			user=authenticate(username=username,password=password) # permission to login
			login(request,user)
			form.save()
			notification="Welcome to Timiza mall.To know more about us have a look at our about page"
			Notification.objects.create(notified=request.user,notification=notification)
			messages.success(request,"Your account has been successfully created.Please check your email for verification")
			return redirect('shop_items_url')
		else:
			return redirect('register')
	else:
		form=RegisterForm()
		return render(request,'account/register.html',{'form':form})


def password_change(request):
	if request.method=="POST":
		form=PasswordChangeForm(request.user,request.POST)
		print(request.POST)
		if form.is_valid():
			form.save()
			notification="Your password has been changed.If you did not do this contact our customer care."
			Notification.objects.create(notified=request.user,notification=notification)
			return redirect('login')		
	else:
		form=PasswordChangeForm(request.user)
		return render(request,'account/change_password.html',{'form':form})