from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail 
import random
import threading
from .middlewares import *
from templates import *
from .forms import *
from .models import *


# Create your views here.
"""
    The function `UserRegister` handles user registration by checking for existing email, validating
    password, creating a new user, sending a registration email, and rendering appropriate messages on
    the webpage.
    
    :param request: The code snippet you provided is a view function in Django for user registration. It
    handles POST requests to register a new user. Here's a breakdown of the code:
    :return: The UserRegister function returns different responses based on the conditions met during
    the POST request handling. Here are the possible return values:
"""
def UserRegister(request):
    if request.method == 'POST':
        if UserAuth.objects.filter(email=request.POST.get('email')):
            return render(request, 'register.html', {'alert' : True})
        else:
            userpassword = request.POST.get('password')
            if CheckPassword(userpassword):
                return render(request, 'register.html', {'error': True}) 
            else:
                newuser = UserAuth.objects.create(
                    email = request.POST.get('email'),
                    name = request.POST.get('name'),
                    message = request.POST.get('message')
                )
                newuser.password = set_password(userpassword)
                send_mail(
                    "Registration Successfull!",
                    
                    f"""Dear {newuser.name},

Welcome to OUR Website! We're excited to have you join our community.

To complete your registration and activate your account, please confirm your email address by clicking the link below:

{newuser.email}

If you didn't register for an account, please ignore this email.

Thank you for choosing OUR Website! If you have any questions or need assistance, feel free to reply to this email or contact our support team.

Best regards,
Mr. Tirth Sharma
OUR Website Team
22bt04139@gsfcuniversity.ac.in """,

                    "dummyforproject09@gmail.com",
                    [newuser.email],
                    fail_silently = False,
                )
                newuser.save()

                return render(request, 'register.html', {'success' : True})
    else:
        success_message = False
        error_message = False
        return render(request, 'register.html', {'success':success_message, 'error': error_message})



"""
    This Python function handles user login authentication and form validation.
    
    :param request: The `request` parameter in the code snippet represents an HTTP request that is
    received by the `UserLogin` view function. It contains information about the incoming request, such
    as the request method (GET, POST, etc.), any data sent in the request (e.g., form data), user
    session
    :return: The UserLogin function returns either a redirect to the 'home' page if the user is
    authenticated successfully, or it returns a rendered login.html template with an alert message if
    the authentication fails or if the form is invalid.
"""
@user_login
@never_cache
def UserLogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                request.session['auth_token'] = 'login'
                request.session['user'] = user.email
                return redirect('home')
            else:
                request.session['auth_token'] = None
                return render(request, 'login.html', {'alert': True, 'form': form})
        else:
            return render(request, 'login.html', {'from': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'alert': False, 'form': form})



"""
    The function `UserHome` logs out the user, retrieves the user's email from the session, removes the
    user from the session, fetches the user's information from the database, and renders the 'home.html'
    template with the user's data.

    :param request: The `request` parameter in the code snippet represents an HTTP request that is sent
    to the server. It contains information about the request made by the client, such as the URL, method
    (GET, POST, etc.), headers, and any data sent with the request. The view function `UserHome
    :return: The UserHome view function is returning a rendered 'home.html' template with the user
    object retrieved from the UserAuth model based on the user's email stored in the session. The user
    object is passed to the template context as 'user'.
"""
@user_logout
@never_cache
def UserHome(request):
    useremail = request.session.get('user')
    user = UserAuth.objects.filter(email = useremail)
    return render(request, 'home.html', {'user': user[0]})



"""
    The `ForgetPassword` function in Python handles the process of sending a one-time password (OTP) for
    password reset to a user's email and verifying the OTP entered by the user.
    
    :param request: The code you provided is a Python function for handling a forget password feature in
    a web application. The function `ForgetPassword` takes a `request` object as a parameter, which is
    typically an HTTP request received by the server
    :return: The code snippet provided is a Python function named `ForgetPassword` that handles the
    logic for resetting a user's password.
"""
@never_cache
def ForgetPassword(request):
    if request.method == 'POST':
        if 'email' in request.POST:
            email = request.POST.get('email')
            user = UserAuth.objects.filter(email=email)

            if user:
                request.session['user_email'] = email
                global otp
                otp = random.randint(100000, 999999)
                send_mail(
                    "Don't Share the OTP!",
                    
                    f"""Dear {user[0].name},

We received a request to reset the password for your account. To proceed with resetting your password, please use the One-Time Password (OTP) provided below:

Your OTP: {otp}

This OTP is valid for the next 40 seconds. Please enter it on the password reset page to create a new password.

If you did not request a password reset, please ignore this email. Your account remains secure, and no changes have been made.

For any concerns or if you need further assistance, please contact our support team.

Best Regards,
OUR Website
22bt04139@gsfcuniversity.ac.in """,
                    "dummyforproject09@gmail.com",
                    [user[0].email],
                    fail_silently = False,
                )
                change_otp_timer = threading.Timer(40.0, ChangeOTP)
                change_otp_timer.start()
                return render(request, 'forget.html', {'alert': 'valid', 'otp_send': True, 'email': email})

            else:
                return render(request, 'forget.html', {'alert': 'invalid', 'email': email})

        elif 'otp' in request.POST:
            get_otp = int(request.POST.get('otp'))
            print("forget",otp)
            try:
                if otp == get_otp:
                    return redirect('reset_password')
                else:
                    return render(request, 'forget.html', {'invalid_otp': True})

            except NameError:
                return render(request, 'forget.html', {'invalid_otp': True})
              
    return render(request, 'forget.html')



"""
    The `ResetPassword` function handles resetting a user's password based on the input provided in a
    POST request.
    
    :param request: The `request` parameter in the `ResetPassword` function is an object that represents
    the HTTP request made by the client. It contains information about the request, such as the method
    used (GET, POST, etc.), any data sent in the request (POST data), session information, user
    authentication details
    :return: The function `ResetPassword` is returning different responses based on the conditions:
"""
@never_cache
def ResetPassword(request):
    if request.method == "POST":
        password = request.POST.get('new-password')
        confirmPassword = request.POST.get('confirm-password')
        if CheckPassword(password):
            return render(request, 'reset.html', {'invalid_password': True})

        elif password != confirmPassword:
            return render(request, 'reset.html', {'confirm_password': True})

        else:
            get_user = UserAuth.objects.get(email=request.session.get('user_email'))
            get_user.password = set_password(password)
            get_user.save()
            request.session.pop('user_email', None)
            return redirect('login')
    return render(request, 'reset.html')


"""
    The `ResendOTP` function sends a one-time password (OTP) to the user's email for password reset and
    starts a timer to change the OTP after 40 seconds.
    
    :param request: The `request` parameter in the `ResendOTP` function is typically an HttpRequest
    object that represents the current request from the user. It contains information about the request,
    such as the user session, user input data, and other metadata related to the request
    :return: The function `ResendOTP` is returning a rendered HTML template named 'forget.html' with a
    context containing the keys 'alert', 'otp_send', and 'email'. The 'alert' key is set to 'valid',
    'otp_send' key is set to True, and the 'email' key is set to the email retrieved from the session.
"""
def ResendOTP(request):
    email = request.session.get('user_email')
    user = UserAuth.objects.get(email = email)
    global otp
    otp = random.randint(100000, 999999)
    send_mail(
        "Don't Share the OTP!",
        
        f"""Dear {user.name},

We received a request to reset the password for your account. To proceed with resetting your password, please use the One-Time Password (OTP) provided below:

Your OTP: {otp}

This OTP is valid for the next 40 seconds. Please enter it on the password reset page to create a new password.

If you did not request a password reset, please ignore this email. Your account remains secure, and no changes have been made.

For any concerns or if you need further assistance, please contact our support team.

Best Regards,
OUR Website
22bt04139@gsfcuniversity.ac.in """,
        "dummyforproject09@gmail.com",
        [user.email],
        fail_silently = False,
    )
    print(otp)
    change_otp_timer = threading.Timer(40.0, ChangeOTP)
    change_otp_timer.start()
    return render(request, 'forget.html', {'alert': 'valid', 'otp_send': True, 'email': email})



"""
    The function UserSignout logs out a user by setting the auth_token to 'logout, removing the user
    session, and redirecting to the login page.
    
    :param request: The `request` parameter in the `UserSignout` function is typically an object that
    contains information about the current HTTP request. It includes details such as the user making the
    request, any data being sent with the request, session information, and more. In this specific
    function, the `request`
    :return: The code snippet is a Python function named `UserSignout` that handles user sign out
    functionality. It sets the value of the 'auth_token' key in the session to 'logout', removes the
    'user' key from the session (if it exists), and then redirects the user to the 'login' page.
"""
def UserSignout(request):
    request.session['auth_token'] = 'logout'
    request.session.pop('user', None)
    return redirect('login')




def ChangeOTP():
    global otp
    otp = 0

def error_404_view(request, exception):
    return render(request, '404.html')