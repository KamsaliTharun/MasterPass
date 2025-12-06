from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

import time

def clear_messages(request):
    storage = messages.get_messages(request)
    storage.used = True


def register(request):
    context = {}

    if request.method == 'POST':
        un = request.POST.get("username")
        pw = request.POST.get("password")
        cpw = request.POST.get("confirm_password")

        # Empty username
        if not un:
            context['username_error'] = "Username cannot be empty"

        if not pw:
            context['password_error'] = "Password cannot be empty"

        if not cpw:
            context['confirm_password_error'] = "Confirm password cannot be empty"

        if context:
            return render(request, 'register.html', context)

        if User.objects.filter(username=un).exists():
            context['username_error'] = "Username already exists"
            return render(request, 'register.html', context)

        if len(pw) < 6:
            context['password_error'] = "Password must be at least 6 characters"
            return render(request, 'register.html', context)

        if pw != cpw:
            context['confirm_password_error'] = "Passwords do not match"
            return render(request, 'register.html', context)

        User.objects.create_user(username=un, password=pw)

        return redirect('register_success')

    return render(request, 'register.html')


def register_success(request):
    return render(request, 'register_success.html')

def password_reset_success(request):
    return render(request, 'password_reset_success.html')

def login(request):
    if request.method == 'POST':
        un = request.POST.get("username")
        pw = request.POST.get("password")
        user = authenticate(request, username=un, password=pw)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')



def forgot_password(request):
    if request.method == 'POST':

        action = request.POST.get("action", "")   # detect resend / verify / none

        # -------------------------------------------------
        # STEP 1 → USERNAME SUBMITTED
        # -------------------------------------------------
        if 'username' in request.POST and action == "":
            username = request.POST.get("username")

            try:
                user = User.objects.get(username=username)

                # store username & timestamp
                request.session['reset_username'] = username
                request.session['otp_time'] = time.time()
                request.session['otp'] = "0000"   # fixed OTP for now

                messages.success(request, "OTP sent successfully!")
                return render(request, 'forgot_password.html', {'step': 2})

            except User.DoesNotExist:
                messages.error(request, "Username does not exist")
                return redirect('forgot_password')

        # -------------------------------------------------
        # STEP 2 → RESEND OTP CLICKED
        # -------------------------------------------------
        if action == "resend_otp":
            clear_messages(request)
            if 'reset_username' not in request.session:
                messages.error(request, "Session expired. Please start again.")
                return redirect('forgot_password')

            # Reset OTP timer
            request.session['otp_time'] = time.time()
            request.session['otp'] = "0000"

            messages.success(request, "OTP resent successfully!")
            return render(request, 'forgot_password.html', {'step': 2})

        # -------------------------------------------------
        # STEP 2 → VERIFY OTP SUBMITTED
        # -------------------------------------------------
        if action == "verify_otp":
            clear_messages(request)
            username = request.session.get("reset_username")
            otp_time = request.session.get("otp_time")

            if not username or not otp_time:
                messages.error(request, "Session expired. Please start again.")
                return redirect("forgot_password")

            # Check OTP expiry (10 sec)
            if time.time() - otp_time > 10:
                del request.session['otp_time']
                del request.session['reset_username']
                messages.error(request, "OTP expired! Please start again.")
                return redirect("forgot_password")

            otp_entered = request.POST.get("otp")
            if otp_entered != request.session.get("otp"):
                messages.error(request, "Invalid OTP")
                return render(request, "forgot_password.html", {"step": 2})

            # OTP correct → move to password reset
            return render(request, "forgot_password.html", {"step": 3})

        # -------------------------------------------------
        # STEP 3 → NEW PASSWORD SUBMITTED
        # -------------------------------------------------
        if 'new_password' in request.POST:
            username = request.session.get("reset_username")

            if not username:
                messages.error(request, "Session expired. Please start again.")
                return redirect("forgot_password")

            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match")
                return render(request, "forgot_password.html", {"step": 3})

            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()

                # clear session
                del request.session['reset_username']
                if 'otp_time' in request.session:
                    del request.session['otp_time']

                messages.success(request, "Password updated successfully! Please login.")
                return redirect("login")

            except User.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect("forgot_password")

    # Default → Step 1
    return render(request, "forgot_password.html", {"step": 1})



def reset_password(request):
    """
    Docstring for reset_password
    
    :param request: Description
    user should be logged in to reset password
    """
    if request.method == 'POST':
        pw = request.POST.get("password")
        cpw = request.POST.get("confirm_password")

        if not pw:
            messages.error(request, "Password cannot be empty")
            return render(request, 'reset_password.html')

        if len(pw) < 6:
            messages.error(request, "Password must be at least 6 characters")
            return render(request, 'reset_password.html')

        if pw != cpw:
            messages.error(request, "Passwords do not match")
            return render(request, 'reset_password.html')

        user = request.user
        user.set_password(pw)
        user.save()
        messages.success(request, "Password reset successfully")
        return redirect('password_reset_success')

    return render(request, 'reset_password.html')
    
def logout(request):
    auth_logout(request)
    return redirect('home')