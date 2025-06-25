from django.core.mail import send_mail
from django.conf import settings
import random
from .models import OTP

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_otp_email(user):
    """Send OTP email to user"""
    otp_code = generate_otp()
    
    # Create or update OTP record in database
    OTP.objects.update_or_create(
        user=user,
        defaults={
            'otp': otp_code,
            'is_verified': False
        }
    )
    
    subject = "Your Verification Code"
    message = f"""
    Hello {user.username},
    
    Your verification code is: {otp_code}
    
    This code will expire in 30 minutes.
    """
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
    

def send_welcome_email(user):
    subject = "Welcome to The Tech Institute!"
    message = f"""
Hi {user.first_name or user.username},

🎉 Welcome to The Tech Institute!

We're excited to have you join us as you begin your journey to master Python, Django, backend, and full-stack web development.

Visit your dashboard to start learning!

🚀 http://127.0.0.1:8000/user/dashboard

Cheers,  
The Tech Institute Team
"""
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
