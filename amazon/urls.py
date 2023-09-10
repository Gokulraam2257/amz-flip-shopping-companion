from django.urls import path
from .views import *
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(r'search/amazon/<str:prod>',get_amazon,name='Amazon'),
    path(r'search/flipkart/<str:prod>',get_flipkart,name='Flipkart'),
    path('register',register,name='register'),
    path('',index,name='index'),
    path('dashboard',dashboard,name='dashboard'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('logout', logout_user, name='logout'),
    path('save',save_alert,name='save'),
    path('otp',otp_verify,name='otp'),
]
