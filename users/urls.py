from django.urls import path
from .views import RegisterView
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm
from django.views.generic import TemplateView
from .views import RegisterView
from .views import *
from . import views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('<str:username>-dashboard/', views.dashboard, name='dashboard'),
    path('<str:username>-edit-profile/', views.edit_profile, name='edit_profile'),
   
    
    path('accounts/email-verification-sent/', TemplateView.as_view(template_name="account/email_verification_sent.html"), name="account_email_verification_sent"),

    # Built-in auth views with your custom form
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html',
        form_class=CustomPasswordResetForm
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]








