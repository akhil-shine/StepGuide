from django.shortcuts import render
from django.contrib.auth import login as auth_login ,authenticate, logout
from django.shortcuts import render, redirect
from .models import CustomUser
from .decorators import user_not_authenticated
from .models import CustomUser,UserProfile
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.mail import send_mail

User = get_user_model()

# Create your views here.
def index(request):
    user=request.user
    if request.user.is_authenticated:
        if user.user_type == CustomUser.ADMIN and not request.path == reverse('admindashboard'):
            return redirect(reverse('admindashboard'))
        elif user.user_type == CustomUser.CLIENT and not request.path == reverse('index'):
            return redirect(reverse('index'))
        elif user.user_type == CustomUser.MERCHANT and not request.path == reverse('merchant_dashbord'):
            return redirect(reverse('merchant_dashbord'))
    
    # if request.user.is_authenticated:
    #     messages.warning(request, 'You are already logged in!')
    #     user=request.user
    #     if user.user_type == CustomUser.ADMIN:
    #         messages.success(request, 'Success! Your action was completed.')
    #         return redirect(reverse('admindashboard'))
    #     elif user.user_type == CustomUser.CLIENT:   
    #         return redirect(reverse('index'))
    #     elif user.user_type == CustomUser.MERCHANT:
    #         return redirect(reverse('merchant_dashbord'))
    #     else:
    #         return redirect('/')    
    return render(request,'index.html',)
def about(request):
    return render(request,'about.html',)
def contact(request):
    return render(request,'contact.html',)
# def shop(request):
#     return render(request,'shop.html',)
# def shopsingle(request):
#     return render(request,'shopsingle.html',)
def admindashboard(request):
    user=request.user
    if request.user.is_authenticated:
        if user.user_type == CustomUser.ADMIN and not request.path == reverse('admindashboard'):
            return redirect(reverse('admindashboard'))
        elif user.user_type == CustomUser.CLIENT and not request.path == reverse('index'):
            return redirect(reverse('index'))
        elif user.user_type == CustomUser.MERCHANT and not request.path == reverse('merchant_dashbord'):
            return redirect(reverse('merchant_dashbord'))    
    return render(request,'admindashboard.html',)
def merchant_dashbord(request):
    user=request.user
    if request.user.is_authenticated:
        if user.user_type == CustomUser.ADMIN and not request.path == reverse('admindashboard'):
            return redirect(reverse('admindashboard'))
        elif user.user_type == CustomUser.CLIENT and not request.path == reverse('index'):
            return redirect(reverse('index'))
        elif user.user_type == CustomUser.MERCHANT and not request.path == reverse('merchant_dashbord'):
            return redirect(reverse('merchant_dashbord'))
    return render(request,'merchant_dashbord.html',)
def buy(request):
    return render(request,'buy.html',)
def purchase(request):
    return render(request,'purchase.html',)
def dashboard(request):
    return render(request,'dashboard.html',)


#login & Registration
# def userlogin(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         print(email)  # Print the email for debugging
#         print(password)  # Print the password for debugging

#         if email and password:
#             user = authenticate(request, email=email, password=password)
#             print("Authenticated user:", user)  # Print the user for debugging
#             if user is not None:
#                 auth_login(request, user)
#                 print("User authenticated:", user.email, user.role)
#                 if request.user.role == CustomUser.CLIENT:
#                     print("user is client")
#                     return redirect('http://127.0.0.1:8000/')
#                 elif request.user.role == CustomUser.THERAPIST:
#                     print("user is therapist")
#                     return redirect(reverse('therapist'))
#                 elif request.user.role == CustomUser.ADMIN:
#                     print("user is admin")                   
#                     return redirect(reverse('adminindex'))
#                 else:
#                     print("user is normal")
#                     return redirect('http://127.0.0.1:8000/')

#             else:
#                 error_message = "Invalid login credentials."
#                 return render(request, 'login.html', {'error_message': error_message})
#         else:
#             error_message = "Please fill out all fields."
#             return render(request, 'login.html', {'error_message': error_message})

#     return render(request, 'login.html')

# @user_not_authenticated
# def register(request):
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name', None)
#         last_name = request.POST.get('last_name', None)
#         email = request.POST.get('email', None)
#         phone = request.POST.get('phone', None)
#         password = request.POST.get('pass', None)
#         confirm_password = request.POST.get('cpass', None)
#         role = User.CLIENT

#         if first_name and last_name and email and phone and password and role:
#             if User.objects.filter(email=email).exists():
#                 error_message = "Email is already registered."
#                 return render(request, 'register2.html', {'error_message': error_message})
            
#             elif password!=confirm_password:
#                 error_message = "Password's Don't Match, Enter correct Password"
#                 return render(request, 'register2.html', {'error_message': error_message})

            
#             else:
#             #     else:
#                 user = User(first_name =first_name,last_name=last_name, email=email, phone=phone,role=role)
#                 user.set_password(password)  # Set the password securely
#                 user.is_active=False
#                 user.save()
#                 user_profile = UserProfile(user=user)
#                 user_profile.save()
#                 # activateEmail(request, user, email)
#                 return redirect('login')  
            
#     return render(request, 'register2.html')
# login
def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        user=request.user
        if user.user_type == CustomUser.ADMIN:
            messages.success(request, 'Success! Your action was completed.')
            return redirect(reverse('admindashboard'))
        elif user.user_type == CustomUser.CLIENT:   
            return redirect(reverse('index'))
        elif user.user_type == CustomUser.MERCHANT:
            return redirect(reverse('merchant_dashbord'))
        else:
            return redirect('/')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirect based on user_type
                    if user.user_type == CustomUser.ADMIN:
                        messages.success(request, 'Success! Your action was completed.')
                        return redirect(reverse('admindashboard'))
                    elif user.user_type == CustomUser.CLIENT:
                        
                        return redirect(reverse('index'))
                    elif user.user_type == CustomUser.MERCHANT:
                        return redirect(reverse('merchant_dashbord'))
                    else:
                        return redirect('/')
                else:
                    return HttpResponseRedirect(reverse('login') + '?alert=account_inactive')
            else:
                return HttpResponseRedirect(reverse('login') + '?alert=invalid_credentials')
        else:
            return HttpResponseRedirect(reverse('login') + '?alert=fill_fields')

    # For GET requests or if authentication fails, display the login form
    return render(request, 'login.html')

# Logout Function
def userLogout(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/') 

# Registration
def register(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('index')
    elif request.method == 'POST':

        username = request.POST.get('username', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        cpassword = request.POST.get('confirmPassword', None)
        user_type = CustomUser.CLIENT

        if username and first_name and last_name and email and phone and password and user_type:

            if User.objects.filter(username=username).exists():
                return HttpResponseRedirect(reverse('register') + '?alert=username_is_already_registered')

            elif User.objects.filter(email=email).exists():
                return HttpResponseRedirect(reverse('register') + '?alert=email_is_already_registered')

            elif User.objects.filter(phone_no=phone).exists():
                return HttpResponseRedirect(reverse('register') + '?alert=phone_no_is_already_registered')
            
            elif password != cpassword: 
                return HttpResponseRedirect(reverse('register') + '?alert=passwords_do_not_match')
                

            else:
                user = User(username=username, first_name=first_name, last_name=last_name, email=email, phone_no=phone,user_type=user_type)
                user.set_password(password)  # Set the password securely
                send_welcome_email(user.email, user.username)
                user.save()

                user_profile = UserProfile(user=user)
                user_profile.save()
                return HttpResponseRedirect(reverse('login') + '?alert=registered')

    return render(request, 'register2.html')

def send_welcome_email(email, user_name):

    # login_url = 'http://127.0.0.1:8000/accounts/login/'  # Update with your actual login URL
    # login_button = f'Click here to log in: {login_url}'


    subject = 'SoulCure - Step Guide Registration'
    message = f"Hello {user_name},\n\n"
    message += f"Welcome to StepGuide! We are thrilled to have you as a part of our community. Your journey towards [briefly describe what your platform offers] starts now.\n\n"
    message += f"Your registration is complete, and we're excited to have you join us. Here are your login credentials:\n\n"
    message += f"Email: {email}\n\n"
    # message += "Please take a moment to log in to your account using the provided credentials. Once you've logged in, we encourage you to reset your password to something more secure and memorable.\n\n"
    # message += login_button
    # message += "\n\nSoulCure is committed to providing a safe and supportive environment for both therapists and clients. Together, we can make a positive impact on the lives of those seeking healing and guidance.\n"
    message += "Thank you for joining the Step Guide community. We look forward to your contributions and the positive energy you'll bring to our platform.\n\n"
    message += "Warm regards,\nThe Step Guide Team\n\n"
    


    from_email='akhilshine14@gmail.com'
      # Replace with your actual email
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)


# Mearchant Registration
def mregister(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('index')
    elif request.method == 'POST':
    
        username = request.POST.get('username', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        cpassword = request.POST.get('confirmPassword', None)
        user_type = CustomUser.MERCHANT

        if username and first_name and last_name and email and phone and password and user_type:

            if User.objects.filter(username=username).exists():
                return HttpResponseRedirect(reverse('register') + '?alert=username_is_already_registered')

            elif User.objects.filter(email=email).exists():
                return HttpResponseRedirect(reverse('register') + '?alert=email_is_already_registered')

            elif User.objects.filter(phone_no=phone).exists():
                return HttpResponseRedirect(reverse('register') + '?alert=phone_no_is_already_registered')
            
            elif password != cpassword: 
                return HttpResponseRedirect(reverse('register') + '?alert=passwords_do_not_match')
                

            else:
                user = User(username=username, first_name=first_name, last_name=last_name, email=email, phone_no=phone,user_type=user_type)
                user.set_password(password)  # Set the password securely
                user.save()

                user_profile = UserProfile(user=user)
                user_profile.save()
                return HttpResponseRedirect(reverse('login') + '?alert=registered')

    return render(request, 'm_register.html')


# Edit Profil
def edit_profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    # user_properties = Property.objects.filter(user=request.user)

    if request.method == 'POST':
        # Get the phone number entered by the user
        new_phone_no = request.POST.get('phone_no')

        # Check if the phone number already exists for a different user
        existing_user = UserProfile.objects.filter(user__phone_no=new_phone_no).exclude(user=request.user).first()
        if existing_user:
            error_message = "Phone number is already registered by another user."
            return HttpResponseRedirect(reverse('edit_profile') + f'?alert={error_message}')
        
        if new_phone_no:
            user.phone_no = new_phone_no
            user.save()

        # Update user fields
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()

        new_profile_pic = request.FILES.get('profile_pic')
        if new_profile_pic:
            user_profile.profile_pic = new_profile_pic

        # Update user profile fields
        user_profile.country = request.POST.get('country')
        user_profile.state = request.POST.get('state')
        user_profile.city = request.POST.get('city')
        user_profile.pin_code = request.POST.get('pin_code')
        user_profile.save()

        return redirect('edit_profile')
    context = {
        'user': user,
        'user_profile': user_profile,
    }

    return render(request, 'edit_profile.html',context)
    