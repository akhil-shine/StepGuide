from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login as auth_login ,authenticate, logout
from django.shortcuts import render, redirect
from .models import CustomUser, Product
from .decorators import user_not_authenticated
from .models import CustomUser,UserProfile,Category,Subcategory,Image
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import get_template


User = get_user_model()


# Index Page
def index(request):
    user=request.user
    if request.user.is_authenticated:
        if user.user_type == CustomUser.ADMIN and not request.path == reverse('dashboard1'):
            return redirect(reverse('dashboard1'))
        elif user.user_type == CustomUser.CLIENT and not request.path == reverse('index'):
            return redirect(reverse('index'))
        elif user.user_type == CustomUser.MERCHANT and not request.path == reverse('dashboard2'):
            return redirect(reverse('dashboard2'))
    return render(request,'index.html',)
def about(request):
    return render(request,'about.html',)
def contact(request):
    return render(request,'contact.html',)

# Merchant Dashboard
def dashboard2(request):
    user=request.user
    stdata = Category.objects.filter(status=False)
    if request.user.is_authenticated:
        if user.user_type == CustomUser.ADMIN and not request.path == reverse('dashboard1'):
            return redirect(reverse('dashboard1'))
        elif user.user_type == CustomUser.CLIENT and not request.path == reverse('index'):
            return redirect(reverse('index'))
        elif user.user_type == CustomUser.MERCHANT and not request.path == reverse('dashboard2'):
            return redirect(reverse('dashboard2'))  
    else:
        return redirect(reverse('index'),{'stdata': stdata})
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
        elif user.user_type == CustomUser.MERCHANT and not request.path == reverse('dashboard2'):
            return redirect(reverse('dashboard2'))
    else:
        return redirect(reverse('index')) 
    user_count = User.objects.exclude(is_superuser=True).count() 
    context = {'user_count': user_count} 
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
            return redirect(reverse('dashboard2'))
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
                        return redirect(reverse('dashboard2'))
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
    # user_properties = product.objects.filter(user=request.user)

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
        elif user.user_type == CustomUser.MERCHANT and not request.path == reverse('dashboard2'):
            return redirect(reverse('dashboard2'))
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

    error_message = ''
    new_category = Category.objects.filter(status=False)

    if request.method == 'POST':

        # Create a new Category instance and assign values
            new_category = Category()
            new_category.category_name = request.POST.get('category_name')
            new_category.descriptioncat = request.POST.get('descriptioncat')
            new_category.save()
            
            return redirect("add_category")
    return render(request, "add_category.html")

# sub
def newsubcategory(request):

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
        stock_16_18 = request.POST.get('stock1')
        stock_20_24 = request.POST.get('stock2')
        stock_25_29 = request.POST.get('stock3')
        stock_30_35 = request.POST.get('stock4')
        price = request.POST.get('price')
        price_16_19 = request.POST.get('price1')
        thumbnail = request.FILES.get('thumbnail')

        # Check if 'male' and 'female' checkboxes are selected
        is_male = request.POST.get('male') == 'male'
        is_female = request.POST.get('female') == 'female'

        # Get the selected category and subcategory objects
        category = stdata1[0]
        subcategory = stdata2[0]

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
        )

        newproduct.save()

        images = request.FILES.getlist('product_images1')
        for image in images:
            Image.objects.create(product=newproduct, images=image)

        return redirect("productlist")

    return render(request, "dashboard2.html", {'stdata': stdata})


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
def productlist(request):
    products = Product.objects.all() 
        
    return render(request,'buy.html', {'products': products})

# display in single page
def purchase(request, product_id):
    # Retrieve tips from URL parameters


    user = request.user
    product = get_object_or_404(Product, id=product_id)


    images = Image.objects.filter(product=product)

    context = {
        'product': product,
        'images': images,
        'user': user,
    }

    return render(request, 'purchase.html',context)
