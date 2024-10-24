"""
URL configuration for auth_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from auth_app.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', UserLogin, name='login'),
    path('login/', UserLogin, name='login'),
    path('accounts/login/', UserLogin, name='login'),
    
    path('register/', UserRegister, name='register'),
    path('home/', UserHome, name='home'),
    path('signout/', UserSignout, name='signout'),
    path('forget-password/', ForgetPassword, name='forget_password'),
    path('reset-password/', ResetPassword, name='reset_password'),
    
    path('resend-otp', ResendOTP, name='resend_otp'),
]

handler404 = 'auth_app.views.error_404_view'