# views.py
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm
from django.contrib import messages
from .models import *
from .utils import  *
from django.contrib.auth import login
from django.contrib.auth.models import User
# from django.utils import timezone  
# from django.conf import settings
from .forms import *
# from ratelimit.decorators import ratelimit
from django.contrib.auth.decorators import login_required
from courses.models import Course
from django.http import Http404



class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send OTP email (no need to pass otp_code separately)
            send_otp_email(user)  # Fixed: Now takes just the user object
            
            # Store verification info in session
            request.session['otp_user_id'] = user.id
            request.session['otp_email'] = user.email
            
            messages.info(request, "Verification code sent to your email")
            return redirect('verify_otp')
            
        return render(request, 'users/register.html', {'form': form})


class VerifyOTPView(View):
    def dispatch(self, request, *args, **kwargs):
        # Check if user has permission to access this page
        if 'otp_user_id' not in request.session:
            messages.error(request, "Please complete registration first")
            return redirect('register')  # Or wherever your signup starts
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        # Only show page if coming from registration
        return render(request, 'users/verify_otp.html', {
            'email': request.session.get('otp_email')
        })

    def post(self, request):
        otp_entered = request.POST.get('otp')
        user_id = request.session.get('otp_user_id')
        
        try:
            user = User.objects.get(id=user_id)
            otp_obj = OTP.objects.filter(
                user=user,
                is_verified=False
            ).latest('created_at')
            
            if otp_obj.is_expired():
                messages.error(request, "OTP has expired. Please register again.")
                return redirect('register')
                
            if otp_entered == otp_obj.otp:
                # Verification successful
                otp_obj.is_verified = True
                otp_obj.save()
                user.is_active = True
                user.save()

                send_welcome_email(user)
                
                # Log user in
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                
                # Clear session
                del request.session['otp_user_id']
                del request.session['otp_email']
                
                messages.success(request, "Account verified/created successfully!")
                return redirect('index')
                
            messages.error(request, "Invalid OTP code")
            
        except (User.DoesNotExist, OTP.DoesNotExist):
            messages.error(request, "Session expired. Please register again.")
            return redirect('register')
        
        return render(request, 'users/verify_otp.html')


class ResendOTPView(View):
    def get(self, request):
        if 'otp_user_id' not in request.session:
            messages.error(request, "Invalid request")
            return redirect('register')
            
        try:
            user = User.objects.get(id=request.session['otp_user_id'])
            send_otp_email(user)
            messages.info(request, "New verification code sent")
        except User.DoesNotExist:
            messages.error(request, "Session expired")
            return redirect('register')
            
        return redirect('verify_otp')



@login_required
def dashboard(request, username):
    if username != request.user.username:
        raise Http404("You are not authorized to view this dashboard.")
    
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    enrolled_courses = Course.objects.filter(students=request.user)
    
    context = {
        'profile': profile,
        'enrolled_courses': enrolled_courses,
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def edit_profile(request, username):
    if username != request.user.username:
        raise Http404("You are not authorized to edit this profile.")
    
    profile = request.user.userprofile
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard', username=request.user.username)
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'users/edit_profile.html', {'form': form})
