from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('initialize-payment/<slug:slug>/', views.initialize_payment, name='initialize_payment'),
    path('verify-payment/', views.verify_payment, name='verify-payment'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('gemini/', views.ai_chat_view, name='gemini-ai'),
    path('test-sms/', views.test_sms_view, name='test-sms'),
]