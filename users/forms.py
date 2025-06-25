from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import PasswordResetForm
# from .models import views
from .models import UserProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'avatar']

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            avatar = self.cleaned_data.get('avatar')
            if avatar:
                user.userprofile.avatar = avatar
                user.userprofile.save()
        return user


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Oops This username is already taken.")
        return username



class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("There is no user registered with this email address.")
        return email

    def get_users(self, email):
        # Return only users that match and are active
        return User.objects.filter(email=email, is_active=True)


# forms.py
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'skills', 'avatar']

