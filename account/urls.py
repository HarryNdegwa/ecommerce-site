from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView

from . import views

urlpatterns=[
	path('login/',LoginView.as_view(template_name='account/login.html'),name="login"),
	path('logout/',LogoutView.as_view(),name="logout"),
	path('register/',views.register,name="register"),
	# path('check-password/',views.check_password,name="check_password"),
	path('change-password/',views.password_change,name="change_password")
]