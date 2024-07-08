from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import get_user_model
from showroom.models import Reservation  # Import Reservation model
from .forms import UserRegisterForm
from .models import PasswordResetRequest

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')

def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            
            if user is not None:
                token = get_random_string(length=32)
                PasswordResetRequest.objects.create(user=user, token=token)
                
                reset_link = request.build_absolute_uri('/accounts/reset-password-confirm/') + token
                send_mail(
                    'Password Reset Request',
                    f'Click the link to reset your password: {reset_link}',
                    'from@example.com',
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, 'Password reset email sent. Check your email for instructions.')
                return redirect('login')
            else:
                messages.error(request, 'User with this email does not exist.')
    else:
        form = PasswordResetForm()
    
    return render(request, 'accounts/forgot_password.html', {'form': form})

def reset_password_confirm(request, token):
    reset_request = get_object_or_404(PasswordResetRequest, token=token, used=False)
    if request.method == 'POST':
        form = SetPasswordForm(reset_request.user, request.POST)
        if form.is_valid():
            new_password1 = form.cleaned_data.get('new_password1')
            new_password2 = form.cleaned_data.get('new_password2')
            if new_password1 != new_password2:
                messages.error(request, "Passwords do not match.")
            else:
                if reset_request.user.check_password(new_password1):
                    messages.error(request, "New password cannot be the same as the current password.")
                else:
                    reset_request.user.set_password(new_password1)
                    reset_request.user.save()
                    reset_request.used = True
                    reset_request.save()
                    update_session_auth_hash(request, reset_request.user)  # Important!
                    messages.success(request, 'Your password has been reset successfully.')
                    return redirect('login')
    else:
        form = SetPasswordForm(reset_request.user)
    return render(request, 'accounts/password_reset_confirm.html', {'form': form})

@login_required
def profile(request):
    reservations = Reservation.objects.filter(user=request.user)
    total_reservations = reservations.count()
    pending_reservations = reservations.filter(status='pending').count()
    accepted_reservations = reservations.filter(status='accepted').count()

    context = {
        'user': request.user,
        'reservations': reservations,
        'total_reservations': total_reservations,
        'pending_reservations': pending_reservations,
        'accepted_reservations': accepted_reservations,
    }
    return render(request, 'accounts/profile.html', context)
