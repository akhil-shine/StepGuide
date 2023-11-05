from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login as auth_login ,authenticate, logout
from django.shortcuts import render, redirect
from .models import CustomUser, Product
from .decorators import user_not_authenticated
from .models import CustomUser,UserProfile,Category,Subcategory,Image,Wishlist,BookCart
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import get_template
from django.http import JsonResponse

User = get_user_model()


# Index Page
# def index(request):
#     user=request.user
#     if request.user.is_authenticated:
#         if user.user_type == CustomUser.ADMIN and not request.path == reverse('dashboard1'):
#             return redirect(reverse('dashboard1'))
#         elif user.user_type == CustomUser.CLIENT and not request.path == reverse('index'):
#             return redirect(reverse('index'))
#         elif user.user_type == CustomUser.MERCHANT and not request.path == reverse('mdashboard2'):
#             return redirect(reverse('mdashboard2'))
#     return render(request,'index.html',)

def index(request):
    user = request.user
    user_profile=None

    if request.user.is_authenticated:
        if user.user_type == CustomUser.ADMIN and not request.path == reverse('dashboard1'):
            return redirect(reverse('dashboard1'))
        elif user.user_type == CustomUser.CLIENT and not request.path == reverse('index'):
            return redirect(reverse('index'))
        elif user.user_type == CustomUser.MERCHANT and not request.path == reverse('mdashboard2'):
            return redirect(reverse('mdashboard2'))
        
        # Get the associated user profile
        user_profile = UserProfile.objects.get(user=user)


    context = {
        'user': user,
        'user_profile': user_profile,
    }
    
    return render(request, 'index.html', context)


# def about(request):
#     return render(request,'about.html',)

def about(request):
    user_profile = None  # Initialize user_profile as None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            pass  # Handle the case when the user profile doesn't exist

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'about.html', context)

def contact(request):
    user_profile = None  # Initialize user_profile as None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            pass  # Handle the case when the user profile doesn't exist

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'contact.html', context)


# Merchant Dashboard
def mdashboard2(request):
    user=request.user
    if request.user.is_authenticated:
        if user.user_type == CustomUser.ADMIN and not request.path == reverse('dashboard1'):
            return redirect(reverse('dashboard1'))
        elif user.user_type == CustomUser.CLIENT and not request.path == reverse('index'):
            return redirect(reverse('index'))
        elif user.user_type == CustomUser.MERCHANT and not request.path == reverse('mdashboard2'):
            return redirect(reverse('mdashboard2'))  
    else:
        return redirect(reverse('index'))
    return render(request,'mdashboard2.html',)


# Merchant Product add 
def dashboard2(request):
    user=request.user
    stdata = Category.objects.filter(status=False)
    # if request.user.is_authenticated:
    #     if user.user_type == CustomUser.ADMIN and not request.path == reverse('dashboard1'):
    #         return redirect(reverse('dashboard1'))
    #     elif user.user_type == CustomUser.CLIENT and not request.path == reverse('index'):
    #         return redirect(reverse('index'))
    #     elif user.user_type == CustomUser.MERCHANT and not request.path == reverse('mdashboard2'):
    #         return redirect(reverse('mdashboard2'))  
    # else:
    #     return redirect(reverse('index'),{'stdata': stdata})
    return render(request,'dashboard2.html',{'stdata': stdata})

def get_subcategories(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
        subcategories = Subcategory.objects.filter(category=category)
        data = [{'id': subcategory.id, 'name': subcategory.name} for subcategory in subcategories]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse([], safe=False)


# Admin Dashboard
def dashboard1(request):
    if request.user.is_authenticated:
        user=request.user
        if user.user_type == CustomUser.ADMIN and not request.path == reverse('dashboard1'):
            return redirect(reverse('dashboard1'))
        elif user.user_type == CustomUser.CLIENT and not request.path == reverse('index'):
            return redirect(reverse('index'))
        elif user.user_type == CustomUser.MERCHANT and not request.path == reverse('mdashboard2'):
            return redirect(reverse('mdashboard2'))
    else:
        return redirect(reverse('index')) 
    
    # Total User Count
    user_count = CustomUser.objects.exclude(is_superuser=True).count()

    # Active User Count
    active_user_count = CustomUser.objects.filter(is_active=True).count()

    # Inactive User Count (excluding superuser)
    inactive_user_count = CustomUser.objects.filter(is_active=False).exclude(is_superuser=True).count()

    # Client and Merchant Counts
    client_count = CustomUser.objects.filter(user_type=CustomUser.CLIENT).count()
    merchant_count = CustomUser.objects.filter(user_type=CustomUser.MERCHANT).count()

    context = {
        'user_count': user_count,
        'active_user_count': active_user_count,
        'inactive_user_count': inactive_user_count,
        'client_count': client_count,
        'merchant_count': merchant_count,
    }
    
    return render(request,'dashboard1.html',context)


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

# Login View
def login_view(request):
    if request.user.is_authenticated:
        user = request.user
        if user.user_type == CustomUser.ADMIN:
            return redirect(reverse('dashboard1'))
        elif user.user_type == CustomUser.CLIENT:
            return redirect(reverse('index'))
        elif user.user_type == CustomUser.MERCHANT:
            return redirect(reverse('mdashboard2'))
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
                        messages.success(request, 'Login Success!!')
                        return redirect(reverse('dashboard1'))
                    elif user.user_type == CustomUser.CLIENT:
                        messages.success(request, 'Login Success!!')
                        return redirect(reverse('index'))
                    elif user.user_type == CustomUser.MERCHANT:
                        messages.success(request, 'Login Success!!')
                        return redirect(reverse('mdashboard2'))
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

# Email Note to Client
def send_welcome_email(email, user_name):
    subject = 'Step Guide-Registration Sucess'
    message = f"Hello {user_name},\n\n"
    message += f"Welcome to StepGuide! We are thrilled to have you as a part of our community. Your journey towards [briefly describe what your platform offers] starts now.\n\n"
    message += f"Your registration is complete, and we're excited to have you join us. Here are your login credentials:\n\n"
    message += f"Your username is: {user_name}\n\n"
    # message += "Please take a moment to log in to your account using the provided credentials. Once you've logged in, we encourage you to reset your password to something more secure and memorable.\n\n"
    # message += login_button
    # message += "\n\nSoulCure is committed to providing a safe and supportive environment for both therapists and clients. Together, we can make a positive impact on the lives of those seeking healing and guidance.\n"
    message += "Thank you for joining the Step Guide community. We look forward to your contributions and the positive energy you'll bring to our platform.\n\n"
    message += "Warm regards,\nThe Step Guide Team\n\n"
    

    from_email='stepguide0@gmail.com'
      # Replace with your actual email
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)

def check_user_email(request):
    userd = request.GET.get('email')
    data = {
        "exists": User.objects.filter(email=userd).exists()
    }
    return JsonResponse(data)
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


# Edit Profile
def edit_profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    # user_product = product.objects.filter(user=request.user)

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
            user_profile.save()
            print("profile_get")

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


# def userview(request):
#     # Query all UserProfile objects from the database
#     CustomUser = CustomUser.objects.all()
    
#     # Pass the data to the template
#     context = {'CustomUser': CustomUser}
    
#     # Render the HTML template
#     return render(request, 'userview.html', context)

# def userview(request):
#     # Fetch data from the database
#     users = UserProfile.objects.all()
#     return render(request, 'userview.html', {'users': users})
    
    
# def userview(request):
#     if request.user.is_authenticated:
#         user=request.user
#         if user.user_type == CustomUser.ADMIN and not request.path == reverse('userview'):
#             return redirect(reverse('userview'))
#         elif user.user_type == CustomUser.CLIENT and not request.path == reverse('index'):
#             return redirect(reverse('index'))
#         elif user.user_type == CustomUser.MERCHANT and not request.path == reverse('dashboard2'):
#             return redirect(reverse('dashboard2'))
#     else:
#         return redirect(reverse('index'))
#     # Fetch data from the database, including user roles
#     users = CustomUser.objects.filter(~Q(is_superuser=True), is_active=True)
#     inactive_users = CustomUser.objects.filter(~Q(is_superuser=True), is_active=False)
#     return render(request, 'userview.html', {'users': users,'inactive_users':inactive_users})

# Active Status
def updateStatus(request,update_id):
    updateUser=User.objects.get(id=update_id)
    if updateUser.is_active==True:
        updateUser.is_active=False
    else:
        updateUser.is_active=True
    updateUser.save()
    return redirect('userview')

# Delete User
def deleteUser(request, delete_id):
    delUser=User.objects.get(id=delete_id)
    delUser.delete()
    return redirect('userview')

# User List
def userview(request):
    if request.user.is_authenticated:
        user = request.user
        if user.user_type == CustomUser.ADMIN and not request.path == reverse('userview'):
            return redirect(reverse('userview'))
        elif user.user_type == CustomUser.CLIENT and not request.path == reverse('index'):
            return redirect(reverse('index'))
        elif user.user_type == CustomUser.MERCHANT and not request.path == reverse('mdashboard2'):
            return redirect(reverse('mdashboard2'))
    else:
        return redirect(reverse('index'))

    # Fetch data from the database, including user roles and whether they are active or not
    users = CustomUser.objects.filter(~Q(is_superuser=True))
    return render(request, 'userview.html', {'users': users})



#Active & Deactive Mail 
def disableAccount(request, update_id):
    updateUser = User.objects.get(id=update_id)
    
    # Check if the user is being disabled
    if updateUser.is_active:
        updateUser.is_active = False
        
        # Send an email to the user
        subject = 'Your Account Has Been Deactivated'
        message = 'Your account has been disabled by an administrator.'
        from_email = 'stepguide0@gmail.com'
        recipient_list = [updateUser.email]

        # Load the email template
        email_template = get_template('disable_notification.html')
        email_content = email_template.render()

        send_mail(subject, message, from_email, recipient_list, html_message=email_content)
        
    else:
        updateUser.is_active = True

    updateUser.save()
    return redirect('userview')



def enableAccount(request, update_id):
    updateUser = User.objects.get(id=update_id)
    
    # Check if the user is being enabled
    if not updateUser.is_active:
        updateUser.is_active = True
        
        # Send an email to the user
        subject = 'Your Account Has Been Activated'
        message = 'Your account has been activated by an administrator.'
        from_email = 'stepguide0@gmail.com'
        recipient_list = [updateUser.email]

        # Load the email template for activation
        email_template = get_template('enable_notification.html')
        email_content = email_template.render()

        send_mail(subject, message, from_email, recipient_list, html_message=email_content)
        
    else:
        updateUser.is_active = False

    updateUser.save()
    return redirect('userview')

# add category
def newcategory(request):
    if request.user.is_authenticated:
        user = request.user
        if user.user_type == CustomUser.ADMIN and not request.path == reverse('add_category'):
            return redirect(reverse('add_category'))
        elif user.user_type == CustomUser.CLIENT and not request.path == reverse('index'):
            return redirect(reverse('index'))
        elif user.user_type == CustomUser.MERCHANT and not request.path == reverse('dashboard2'):
            return redirect(reverse('dashboard2'))
    else:
        return redirect(reverse('index'))

    error_message = ''
    new_category = Category.objects.filter(status=False)

    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_description = request.POST.get('descriptioncat')

        # Check if the category name already exists
        if Category.objects.filter(category_name=category_name, status=False).exists():
            return HttpResponseRedirect(reverse('add_category') + '?alert=Error')
        else:
            # Category name is unique; create a new Category instance and save it
            new_category = Category()
            new_category.category_name = category_name
            new_category.descriptioncat = category_description
            new_category.save()
            return HttpResponseRedirect(reverse('add_category') + '?alert=Success')
            # return redirect("add_category")

    return render(request, "add_category.html", {"error_message": error_message})




# sub
def newsubcategory(request):
    if request.user.is_authenticated:
        user = request.user
        if user.user_type == CustomUser.ADMIN and not request.path == reverse('add_subcategory'):
            return redirect(reverse('add_subcategory'))
        elif user.user_type == CustomUser.CLIENT and not request.path == reverse('index'):
            return redirect(reverse('index'))
        elif user.user_type == CustomUser.MERCHANT and not request.path == reverse('mdashboard2'):
            return redirect(reverse('mdashboard2'))
    else:
        return redirect(reverse('index'))

    error_message = ''
    new_category = Category.objects.filter(status=False)

    if request.method == 'POST':
            categories = Category.objects.filter(status=False)
            print('Entered')
            name = request.POST['name']
            category_id = request.POST['category_id']

            print(category_id)
            description = request.POST['description']
            
            category = Category.objects.get(id=category_id)
            subcategory = Subcategory.objects.create(
            name=name,
            description = description,
            category=category,
            )  


    context = {
            'new_category': new_category,
        
            }
    return render(request, "add_subcategory.html",context)

# add product in merchant page
# def sellerindex(request):
#     stdata = Category.objects.filter(status=False)
#     user = request.user
#     userid = user.id

#     if request.method == 'POST':
#         product_name = request.POST.get('product_name')
#         brand_name = request.POST.get('brand_name')
#         product_description = request.POST.get('product_description')
#         material_description = request.POST.get('material_description')
#         measurements = request.POST.get('measurements')
#         maintenance = request.POST.get('maintenance')
#         price = request.POST.get('price')
#         quantity = request.POST.get('quantity')
#         category_name = request.POST.get('category')
#         subcategory_name = request.POST.get('subcategory')
#         gender = request.POST.get('gender')
        
#         # Check if the category and subcategory exist
#         stdata1 = Category.objects.get(name__iexact=category_name)
#         stdata2 = Subcategory.objects.get(name__iexact=subcategory_name)

#         # Create a new Product instance and assign values
#         new_product = Product(
#             product_name=product_name,
#             brand_name=brand_name,
#             product_description=product_description,
#             material_description=material_description,
#             measurements=measurements,
#             maintenance=maintenance,
#             price=price,
#             quantity=quantity,
#             category_name=stdata1,
#             subcategory_name=stdata2,
#             gender=gender,
            
#             stock_16_18=request.POST.get('stock16-18'),
#             stock_20_24=request.POST.get('stock20-24'),
#             stock_25_29=request.POST.get('stock25-29'),
#             stock_30_35=request.POST.get('stock30-35'),

#             product_image=request.FILES.get('product_image'),
#             user_id=userid
#         )
#         new_product.save()

#         return redirect("product")
    
#     return render(request, "sellerindex.html", {'stdata': stdata})

# def sellerindex(request):
    
#     stdata = Category.objects.filter(status=False)
#     category_name = request.POST.get('category')
#     sub = request.POST.get('subcategory')
#     stdata1 = Category.objects.filter(pk__iexact=category_name)
#     stdata2 = Subcategory.objects.filter(pk__iexact=sub)
#     user = request.user
#     userid = user.id
#     if request.method == 'POST':
#         print(request.POST.get('brand_name'))
#         print(request.POST.get('category'))
#         print(request.POST.get('subcategory'))
#         # Create a new Category instance and assign values
#         newproduct =    Product(
#         brand_name = request.POST.get('brand_name'),
#         product_description= request.POST.get('product_description'),
#         material_description= request.POST.get('material_description'),
#         stock_16_18= request.POST.get('stock1'),
#         stock_20_24= request.POST.get('stock2'),
#         stock_25_29= request.POST.get('stock3'),
#         stock_30_35= request.POST.get('stock4'),
#         price= request.POST.get('price'),
#         price_16_19= request.POST.get('price1'),
#         male = request.POST.get('male') == 'male',
#         female = request.POST.get('female') == 'female',
#         thumbnail= request.FILES.get('thumbnail'),


#         category = stdata1[0],
#         subcategory = stdata2[0],


#         user_id=userid
#         )
#         newproduct.save() 

        
#         images = request.FILES.getlist('product_images1')
#         for image in images:
#             Image.objects.create(product=newproduct,images=image)
            
#         return redirect("dashboard2")
#     return render(request, "dashboard2.html",{'stdata':stdata})


def sellerindex(request):
    stdata = Category.objects.filter(status=False)
    category_name = request.POST.get('category')
    sub = request.POST.get('subcategory')
    stdata1 = Category.objects.filter(pk__iexact=category_name)
    stdata2 = Subcategory.objects.filter(pk__iexact=sub)
    user = request.user
    userid = user.id

    if request.method == 'POST':
        brand_name = request.POST.get('brand_name')
        product_description = request.POST.get('product_description')
        material_description = request.POST.get('material_description')
        stock_16_18 = int(request.POST.get('stock1', 0))  # Convert to int with default value 0
        stock_20_24 = int(request.POST.get('stock2', 0))  # Convert to int with default value 0
        stock_25_29 = int(request.POST.get('stock3', 0))  # Convert to int with default value 0
        stock_30_35 = int(request.POST.get('stock4', 0))  # Convert to int with default value 0
        price = request.POST.get('price')
        price_16_19 = request.POST.get('price1')
        thumbnail = request.FILES.get('thumbnail')

        # Check if 'male' and 'female' checkboxes are selected
        is_male = request.POST.get('male') == 'male'
        is_female = request.POST.get('female') == 'female'

        # Get the selected category and subcategory objects
        category = stdata1[0]
        subcategory = stdata2[0]
        total_stock = stock_16_18 + stock_20_24 + stock_25_29 + stock_30_35
        # Create a new Product instance and assign values
        newproduct = Product(
            user=user,
            brand_name=brand_name,
            category=category.category_name,  # Save category name
            subcategory=subcategory.name,  # Save subcategory name
            product_description=product_description,
            material_description=material_description,
            male=is_male,
            female=is_female,
            stock_16_18=stock_16_18,
            stock_20_24=stock_20_24,
            stock_25_29=stock_25_29,
            stock_30_35=stock_30_35,
            price=price,
            price_16_19=price_16_19,
            thumbnail=thumbnail,
            total_stock=total_stock,
        )

        newproduct.save()

        images = request.FILES.getlist('product_images1')
        for image in images:
            Image.objects.create(product=newproduct, images=image)

        return redirect("productlist")

    return render(request, "mdashboard2.html", {'stdata': stdata})


def categoryajax(request, category):
    stdata1 = Subcategory.objects.filter(category_id=category).values('name')

    # Extract the values from the queryset and add them to the data list
    data = []
    for item in stdata1:
        data.extend(item.values())

    # Print the data for debugging (optional)
    print(data)
    
    # Return the data as a JSON response
    return JsonResponse(data,safe=False)

# for display product
# def productlist(request):
#     products = Product.objects.all()
#     wishlist_items = []
#     wishlist_product_ids = []
#     user_cart_ids = []

#     if request.user.is_authenticated:
#         wishlist_items = Wishlist.objects.filter(user=request.user)
#         wishlist_product_ids = wishlist_items.values_list('product_id', flat=True)
#         user_cart = BookCart.objects.filter(user=request.user)
#         user_cart_ids = [item.product.id for item in user_cart]
        
#         # Get the associated user profile
#         user_profile = UserProfile.objects.get(user=request.user)
#         context = {
#         'user': request.user,  # Use request.user instead of user
#         'user_profile': user_profile,
#     }
#     return render(request, 'buy.html', {
#         'products': products,
#         'wishlist_items': wishlist_items,
#         'wishlist_product_ids': wishlist_product_ids,
#         'user_cart_ids': user_cart_ids,
#     })

# Buy.html page
def productlist(request):
    products = Product.objects.all()
    wishlist_items = []
    wishlist_product_ids = []
    user_cart_ids = []
    user_profile = None  # Initialize user_profile as None

    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        wishlist_product_ids = wishlist_items.values_list('product_id', flat=True)
        user_cart = BookCart.objects.filter(user=request.user)
        user_cart_ids = [item.product.id for item in user_cart]
        
        # Get the associated user profile
        user_profile = UserProfile.objects.get(user=request.user)

    context = {
        'products': products,
        'wishlist_items': wishlist_items,
        'wishlist_product_ids': wishlist_product_ids,
        'user_cart_ids': user_cart_ids,
        'user': request.user,
        'user_profile': user_profile,
    }
    
    return render(request, 'buy.html', context)


# display in single page
def purchase(request, product_id):
    # Retrieve tips from URL parameters


    user = request.user
    product = get_object_or_404(Product, id=product_id)
    
            # Get the associated user profile
    user_profile = UserProfile.objects.get(user=request.user)


    images = Image.objects.filter(product=product)

    context = {
        'product': product,
        'images': images,
        'user': user,
        'user_profile': user_profile,
    }

    return render(request, 'purchase.html',context)

# for display men_only_product
def menonly(request):
    products = Product.objects.filter(male=True) 
        
    return render(request,'men_only.html', {'products': products})

# for display women_only_product
def womenonly(request):
    products = Product.objects.filter(female=True) 
        
    return render(request,'women_only.html', {'products': products})

# for display kids_only_product
def kidsonly(request):
    products = Product.objects.filter(stock_16_18__gt=0)
        
    return render(request,'kids_only.html', {'products': products})

# wishlist
def delete_wishlist(request, product_id):
    wishlist_item = get_object_or_404(Wishlist, product_id=product_id, user=request.user)
    wishlist_item.delete()
    return redirect('productlist')

def wishlist_view(request):
    if request.user.is_authenticated:
        # Retrieve the wishlist items for the logged-in user
        wishlist_items = Wishlist.objects.filter(user=request.user)
        # Extract the product from the wishlist items
        wishlist_product = [item.product for item in wishlist_items]
                # Get the user's profile
        user_profile = UserProfile.objects.get(user=request.user)
        return render(request, 'wishlist.html', {'wishlist_product': wishlist_product, 'user_profile': user_profile})
    else:
        # Handle the case when the user is not logged in
        # You can redirect them to the login page or display a message
        return render(request, 'wishlist.html', {'wishlist_product': None})
    
def add_wishlist(request, product_id):
    # Get the product object based on the product_id
    product = get_object_or_404(Product, id=product_id)

    # Create a Wishlist object for the current user and the product
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        if created:
            message = f'The product "{product.brand_name}" has been added to your wishlist.'
        else:
            message = f'The product "{product.brand_name}" is already in your wishlist.'
    else:
        # Handle the case where the user is not authenticated
        message = 'You need to be logged in to add Products to your wishlist.'

    # You can pass the message to your template or use it as needed
    # For now, we'll just redirect back to the productlist view
    return redirect('productlist')

# cart
def cart(request):
    # Assuming you have the user object for the currently logged-in user
    user_id = request.user.id  # Replace with your user retrieval logic if needed
    # Retrieve books in the user's cart
    books_in_cart = BookCart.objects.filter(user_id=user_id)
    products3 = Category.objects.filter(status=False)
    
    user_profile = UserProfile.objects.get(user=request.user)

# Retrieve book details for the books in the cart
    book_details = Product.objects.filter(id__in=books_in_cart.values_list('product_id', flat=True))
    print(book_details)
    print("hai")
    total_price = sum(books_in_cart.product.price * books_in_cart.quantity for books_in_cart in books_in_cart)
    
    #product_id=BookCart.request.get(product_id=product_id)
    st = BookCart.objects.filter(user_id=user_id)
    return render(request,"cart.html",{'cart_books':book_details,'st':st,'total_price':total_price,'products3':products3,'user_profile': user_profile,})

def increase_item(request, item_id):
    try:
        cart_item = BookCart.objects.get(product_id=item_id)
        product = Product.objects.get(id=cart_item.product_id)

        # Calculate the new quantity, ensuring it doesn't exceed the product's quantity
        new_quantity = min(int(cart_item.quantity) + 1, int(product.total_stock))

        cart_item.quantity = str(new_quantity)
        cart_item.save()
    except BookCart.DoesNotExist:
        pass  # Handle the case when the item does not exist in the cart
    except Product.DoesNotExist:
        pass  # Handle the case when the associated product doesn't exist

    return redirect('cart')

def decrease_item(request, item_id):
    try:
        cart_item = BookCart.objects.get(product_id=item_id)
        
        # Decrease the quantity by 1, but ensure it doesn't go below 1
        new_quantity = max(int(cart_item.quantity) - 1, 1)
        
        cart_item.quantity = str(new_quantity)
        cart_item.save()
    except BookCart.DoesNotExist:
        pass  # Handle the case when the item does not exist in the cart

    return redirect('cart')

def add_cart(request, bookid2):
    userid=request.user.id
    product = get_object_or_404(Product, id=bookid2)
    cart_item, created = BookCart.objects.get_or_create(user=request.user,product_id=product.id)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('productlist')

def delete_cart(request, bookid2):
    remove=BookCart.objects.filter(product_id=bookid2)
    remove.delete()
    return redirect('cart')


def add_cart1(request, bookid2):
    userid=request.user.id
    product = get_object_or_404(Product, id=bookid2)
    cart_item, created = BookCart.objects.get_or_create(user=request.user,product_id=product.id)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

        # Redirect to 'singleview' with the 'bookid' parameter
    return redirect('purchase',product_id=product.id)
    


# Search
def search_product(request):
    query = request.GET.get('query')
    print("Query:", query)

   
    if query:
        product = Product.objects.filter(
            Q(brand_name__icontains=query) | Q(category__icontains=query) | Q(subcategory__icontains=query) | Q(price__icontains=query) | Q(price_16_19__icontains=query)
        )
    else:
       
        product = []
    product_data = []
    
    for product in product:
        
        product_dict = {
            'id': product.pk,
            'thumbnail': product.thumbnail.url,
            'brand_name':  product.brand_name,
            'category':  product.category,
            'subcategory':  product.subcategory,
            'price_16_19':  product.price_16_19,
            'price':  product.price,
        }
        product_data.append(product_dict)

    return JsonResponse({'product': product_data})