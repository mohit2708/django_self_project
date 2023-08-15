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
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        # Create the user
        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password1)

         # Create the user profile
        UserProfile.objects.create(
            user=user,
            age=age,
            gender=gender,
        )
        user.save()
        
        messages.success(request, "Registration successful. You can now log in.")
        return redirect('login')  # Redirect to login page after successful registration
    
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