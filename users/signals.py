from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .utils import send_welcome_email

@receiver(user_signed_up)
def handle_social_signup(sender, request, user, **kwargs):
    # Only send on first-time signup
    send_welcome_email(user)
