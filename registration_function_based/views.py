# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import UserProfile
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist  #Import the exception
# email
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string

from django.contrib.auth import update_session_auth_hash

import random
import string
from datetime import timedelta
from django.utils import timezone
from .models import ResetToken

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
import datetime 




def send_email(request):
    # subject = 'Subject of the Email'
    # message = 'This is the message body of the email.'
    # from_email = 'your_email@gmail.com'
    # recipient_list = ['mksaxena27@yopmail.com']

    # send_mail(subject, message, from_email, recipient_list)
    
    # # Optionally, you can also specify a fail_silently parameter:
    # # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    
    # return HttpResponse('Email sent successfully.')

    subject = 'Subject of the Email'
    template = 'registration_function_based/email_template.html'
    context = {'variable': 'Value for the template'}

    message = render_to_string(template, context)
    from_email = 'your_email@gmail.com'
    recipient_list = ['mksaxena27@yopmail.com']

    send_mail(subject, message, from_email, recipient_list, html_message=message)
    
    return HttpResponse('Email sent successfully.')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        age = request.POST['age']
        gender = request.POST['gender']

        value = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'email': email,
            'age': age,
            'gender': gender
        }
        error_messages = {}

        if not first_name:
            error_messages['first_name'] = "First name is required!"
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')
        
        if not error_messages:
        # Create the user
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password1)

            # Create the user profile
            UserProfile.objects.create(
                user=user,
                age=age,
                gender=gender,
            )
            user.save()
        else:
            context = {'error':error_messages,'values':value}
            return render(request, 'registration_function_based/register.html', context)
        
        messages.success(request, "Registration successful. You can now log in.")
        return redirect('login')  # Redirect to login page after successful registration
    # context = {'values':value}
    return render(request, 'registration_function_based/register.html')



# This decorator checks if the user is not authenticated (not logged in)
@user_passes_test(lambda u: not u.is_authenticated, login_url='home')
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('home')  # Redirect to the home page after successful login
        else:
            messages.error(request, "Invalid login credentials.")
    
    return render(request, 'registration_function_based/login.html')


# @login_required(login_url='login')  # Redirect unauthorized users to the login page
def home(request):
    context = {}
    
    if request.user.is_authenticated:
        user = request.user
        try:
            profile = user.userprofile  # Assuming your UserProfile model has a related_name='userprofile'
        except ObjectDoesNotExist:
            profile = None  # Set profile to None if it doesn't exist
        context = {
            'user': user,
            'profile': profile,
        }
    
    return render(request, 'registration_function_based/home.html', context)

def custom_logout(request):
    logout(request)
    return redirect('home')




@login_required
def custom_change_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        user = request.user
        if not user.check_password(old_password):
            return render(request, 'registration_function_based/change_password.html', {'status_message': 'Old password is incorrect.'})
        elif new_password1 != new_password2:
            return render(request, 'registration_function_based/change_password.html', {'status_message': 'New passwords do not match.'})
        else:
            user.set_password(new_password1)
            user.save()
            update_session_auth_hash(request, user)  # Important to update session
            return render(request, 'registration_function_based/change_password.html', {'status_message': 'Password changed successfully.'})
    else:
        return render(request, 'registration_function_based/change_password.html', {'status_message': ''})

User = get_user_model()

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        reset_link = request.build_absolute_uri(f'/registration_function_based/reset-password/{user.pk}/{token}/')

        reset_token = ResetToken(user=user, token=token, expires_at=datetime.datetime.now() + datetime.timedelta(hours=24))
        reset_token.save()
        
        print(reset_link)
        send_reset_email(user, reset_link)
        return render(request, 'registration_function_based/forgot_password.html')
    return render(request, 'registration_function_based/forgot_password.html')

def reset_password_request(request):
    if request.method == 'POST':
        email = request.POST['email']
        
        # Check if user with the provided email exists
        user = User.objects.filter(email=email).first()
        if user:
            # Generate a unique reset token and send the reset email
            reset_token = generate_reset_token(user)
            send_reset_email(user, reset_token)
            
            return redirect('reset_password_done')
        else:
            return render(request, 'registration_function_based/forgot_password.html', {'status_message': 'Email not found.'})
    else:
        return render(request, 'registration_function_based/forgot_password.html', {'status_message': ''})

def reset_password_confirm(request, user_id, reset_token):
    print(f"User ID: {user_id}, Token: {reset_token}")

    user = get_user_from_reset_token(reset_token)
    try:
            reset_token_obj = ResetToken.objects.get(user=user, token=reset_token)
    except ResetToken.DoesNotExist:
            return render(request, 'registration_function_based/password_reset_failed.html')
    if user:
        print('user aa gya')
        if request.method == 'POST':
            new_password = request.POST['new_password']
            user.set_password(new_password)
            user.save()
            reset_token_obj.delete()
            return render(request, 'registration_function_based/password_reset_success.html')
        else:
            return render(request, 'registration_function_based/reset_password_confirm.html', {'reset_token': reset_token})
    else:
        print("Token validation failed")
        return render(request, 'registration_function_based/password_reset_failed.html')

def send_reset_email(user, reset_token):
    subject = 'Password Reset'
    message = f'Click the following link to reset your password: {reset_token}'
    from_email = 'your_email@example.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


def generate_reset_token(user):
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=40))
    expiration_time = timezone.now() + timedelta(hours=24)  # Token expires in 24 hours
    ResetToken.objects.create(user=user, token=token, expires_at=expiration_time)
    return token

def get_user_from_reset_token(reset_token):
    try:
        reset_token_obj = ResetToken.objects.get(token=reset_token, expires_at__gt=timezone.now())
        return reset_token_obj.user
    except ResetToken.DoesNotExist:
        return None
    
def reset_password_done(request):
    return render(request, 'registration_function_based/reset_password_done.html')

def password_reset_success(request):
    return render(request, 'registration_function_based/password_reset_success.html')


def password_reset_failed(request):
    return render(request, 'registration_function_based/password_reset_failed.html')
