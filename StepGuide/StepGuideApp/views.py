import random
import string
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login as auth_login ,authenticate, logout
from django.shortcuts import render, redirect
from .models import AgentProfile, CustomUser, Product, ProductReturn
from .decorators import user_not_authenticated
from .models import CustomUser,UserProfile,Category,Subcategory,Image,Wishlist,BookCart,SizeStock,Cart,CartItem,Order, OrderItem, Rating, CompareProduct,Notification,NewArrival
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import get_template
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Subcategory
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Product, Wishlist, BookCart
from decimal import Decimal
from django.http import HttpResponseRedirect
from decimal import Decimal, InvalidOperation, ConversionSyntax
from .models import ShippingAddress
from django.conf import settings
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
from django import forms
from django.utils import timezone
from .forms import NewArrivalForm, ProductReturnForm
from django.core.exceptions import ObjectDoesNotExist




razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


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
        elif user.user_type == CustomUser.AGENT and not request.path == reverse('adashboard'):
            return redirect(reverse('adashboard'))
        
        # Get the associated user profile
        # user_profile = UserProfile.objects.get(user=user)


    context = {
        'user': user,
        'user_profile': user_profile,
    }
    
    return render(request, 'index.html', context)


# def about(request):
#     return render(request,'about.html',)

def about(request):
    return render(request,'about.html',)
def contact(request):
    return render(request,'contact.html',)


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
        elif user.user_type == CustomUser.AGENT and not request.path == reverse('adashboard'):
            return redirect(reverse('adashboard')) 
    else:
        return redirect(reverse('index'))
    merchant_products = Product.objects.filter(user=request.user)
    product_count = merchant_products.count()
    agent_count = CustomUser.objects.filter(user_type=CustomUser.AGENT).count()
    
    notifications = Notification.objects.filter(
    recipient=request.user, is_read=False)
    
    
    return render(request,'mdashboard2.html',{'notifications': notifications,'merchant_products': merchant_products, 'product_count': product_count, 'agent_count': agent_count})
    


# Merchant Product add 
@login_required
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
        elif user.user_type == CustomUser.AGENT and not request.path == reverse('adashboard'):
            return redirect(reverse('adashboard'))
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
    agent_count = CustomUser.objects.filter(user_type=CustomUser.AGENT).count()

    context = {
        'user_count': user_count,
        'active_user_count': active_user_count,
        'inactive_user_count': inactive_user_count,
        'client_count': client_count,
        'merchant_count': merchant_count,
        'agent_count': agent_count
    }
    
    return render(request,'dashboard1.html',context)


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
        elif user.user_type == CustomUser.AGENT:
            return redirect(reverse('adashboard'))
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
@login_required
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
        existing_category = Category.objects.filter(category_name__iexact=category_name)
        if existing_category.filter(status=False).exists():
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




# subcategory
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
        category_id = request.POST.get('category_id')
        subcategory_name = request.POST.get('name')
        subcategory_description = request.POST.get('description')

        # Check if the subcategory name already exists within the specified category
        existing_subcategory = Subcategory.objects.filter(name__iexact=subcategory_name, category_id=category_id)
        if existing_subcategory.exists():
            return HttpResponseRedirect(reverse('add_subcategory') + '?alert=Error')
        else:
            # Subcategory name is unique within the category; create a new Subcategory instance and save it
            category = Category.objects.get(id=category_id)
            new_subcategory = Subcategory()
            new_subcategory.name = subcategory_name
            new_subcategory.description = subcategory_description
            new_subcategory.category = category
            new_subcategory.save()
            return HttpResponseRedirect(reverse('add_subcategory') + '?alert=Success')

    return render(request, "add_subcategory.html", {"new_category": new_category, "error_message": error_message})



# Manage Categories
def manage_categories(request):
    if request.user.is_authenticated:
        categories = Category.objects.filter(status=False)
        subcategories = Subcategory.objects.all()
        
        if request.method == 'POST':
            if 'delete_category' in request.POST:
                category_id = request.POST.get('category_id')
                category = get_object_or_404(Category, id=category_id)
                category.delete()
                return redirect('manage_categories')
            
            if 'delete_subcategory' in request.POST:
                subcategory_id = request.POST.get('subcategory_id')
                subcategory = get_object_or_404(Subcategory, id=subcategory_id)
                subcategory.delete()
                return redirect('manage_categories')

        context = {
            'categories': categories,
            'subcategories': subcategories,
        }
        return render(request, "manage_categories.html", context)
    else:
        return redirect('index')


# add new product
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
        stock_16_18 = request.POST.get('stock1',0)  # Convert to int with default value 0
        stock_20_24 = request.POST.get('stock2',0)  # Convert to int with default value 0
        stock_25_29 = request.POST.get('stock3',0)  # Convert to int with default value 0
        price = request.POST.get('price')
        price_16_19 = request.POST.get('price1')
        thumbnail = request.FILES.get('thumbnail')

        # Check if 'male' and 'female' checkboxes are selected
        is_male = request.POST.get('male') == 'male'
        is_female = request.POST.get('female') == 'female'

        # Get the selected category and subcategory objects
        category = stdata1[0]
        subcategory = stdata2[0]




        # Set default values to 0 if they are empty or None
        stock_16_18 = stock_16_18 if stock_16_18 else '0'
        stock_20_24 = stock_20_24 if stock_20_24 else '0'
        stock_25_29 = stock_25_29 if stock_25_29 else '0'

        # Convert to integers
        stock_16_18 = int(stock_16_18)
        stock_20_24 = int(stock_20_24)
        stock_25_29 = int(stock_25_29)

        total_stock = stock_16_18 * (3 * 6) + stock_20_24 * (5 * 6) + stock_25_29 * (4 * 6)

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
            stock_for_child_1_3=stock_16_18,
            stock_4_8=stock_20_24,
            stock_9_12=stock_25_29,
            price=price,
            price_16_19=price_16_19,
            thumbnail=thumbnail,
            total_stock=total_stock,
        )

        newproduct.save()

        images = request.FILES.getlist('product_images1')
        for image in images:
            Image.objects.create(product=newproduct, images=image)

        # Add rows to SizeStock based on conditions
        sizes_and_stocks = [
            ('Size 1-3', stock_16_18, 3),
            ('Size 4-8', stock_20_24, 5),
            ('Size 9-12', stock_25_29, 4),
        ]

        for size_name, stock_quantity, multiplier in sizes_and_stocks:
            for i in range(1, multiplier + 1):
                serial_number = i + (0 if '1-3' in size_name else 3 if '4-8' in size_name else 8)
                SizeStock.objects.create(
                    product=newproduct,
                    size=f"{serial_number}",
                    stock_quantity=stock_quantity * 6
                )

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


# @login_required
def productlist(request):
    products = Product.objects.all()
    wishlist_items = []
    wishlist_product_ids = []
    user_cart_ids = []

    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        wishlist_product_ids = wishlist_items.values_list('product_id', flat=True)
        user_cart = BookCart.objects.filter(user=request.user)
        user_cart_ids = [item.product.id for item in user_cart]
        
        # Get the associated user profile

    context = {
        'products': products,
        'wishlist_items': wishlist_items,
        'wishlist_product_ids': wishlist_product_ids,
        'user_cart_ids': user_cart_ids,
        'user': request.user,
    }
    
    return render(request, 'buy.html', context)

# Product filter
@login_required
def filter_products(request):
    # Retrieve all products
    products = Product.objects.all()

    # Retrieve wishlist items for the authenticated user
    wishlist_items = []
    wishlist_product_ids = []
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        wishlist_product_ids = wishlist_items.values_list('product_id', flat=True)

    # Retrieve user's cart items
    user_cart = BookCart.objects.filter(user=request.user)
    user_cart_ids = [item.product.id for item in user_cart]

    # Apply filters based on user preferences
    brand_filter = request.GET.get('brand')
    category_filter = request.GET.get('category')

    # Price range filters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if brand_filter:
        products = products.filter(brand_name=brand_filter)

    if category_filter:
        products = products.filter(category=category_filter)

    try:
        if min_price is not None:
            min_price = max(0, Decimal(min_price))
            print(f"Applied min_price filter: {min_price}")
            products = products.filter(price__gte=min_price)

        if max_price is not None:
            max_price = Decimal(max_price)
            print(f"Applied max_price filter: {max_price}")
            products = products.filter(price__lte=max_price)

    except InvalidOperation as e:
        print(f"Error converting min_price or max_price to Decimal: {e}")
    except ConversionSyntax as e:
        print(f"Error in decimal conversion: {e}")

    print(f"Number of products before filters: {Product.objects.count()}")
    print(f"Number of products after filters: {products.count()}")

    context = {
        'products': products,
        'wishlist_items': wishlist_items,
        'wishlist_product_ids': wishlist_product_ids,
        'user_cart_ids': user_cart_ids,
        'user': request.user,
    }

    return render(request, 'buy.html', context)





# display in single page
@login_required
def purchase(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    avg_rating = Rating.objects.filter(products=product).aggregate(avg_rating=Avg('value'))
    comments = Rating.objects.filter(products=product).exclude(comment__exact='')

    # Select sizes with stock_quantity > 0 for the specific product_id
    sizes_with_stock = SizeStock.objects.filter(product=product, stock_quantity__gt=0)

    images = Image.objects.filter(product=product)
    
    compare_product = CompareProduct.objects.filter(user=user).first()
    compare_product_list = compare_product.Product.all() if compare_product else []

    context = {
        'product': product,
        'images': images,
        'user': user,
        'sizes_with_stock': sizes_with_stock,
        'avg_rating': avg_rating['avg_rating'],
        'comments': comments,
        'compare_product': compare_product_list,  # Pass the compare properties to the context
    }
    if len(compare_product_list) >= 4 and product not in compare_product_list:
        messages.error(request, "You cannot add more properties to compare. Remove a property from compare to add another.")
        context['disable_compare_button'] = True

    return render(request, 'purchase.html', context)

# for display men_only_product
@login_required
def menonly(request):
    products = Product.objects.filter(male=True)
    user_profile = UserProfile.objects.get(user=request.user)

    return render(request, 'men_only.html', {'products': products, 'user': request.user, 'user_profile': user_profile})

# for display women_only_product
@login_required
def womenonly(request):
    products = Product.objects.filter(female=True) 
    return render(request,'women_only.html', {'products': products, 'user': request.user})

# for display kids_only_product
@login_required
def kidsonly(request):
    products = Product.objects.filter(stock_16_18__gt=0)
    return render(request,'kids_only.html', {'products': products, 'user': request.user})

# wishlist
def delete_wishlist(request, product_id):
    wishlist_item = get_object_or_404(Wishlist, product_id=product_id, user=request.user)
    wishlist_item.delete()
    return redirect('productlist')

def delete_wishlist1(request, product_id):
    wishlist_item = get_object_or_404(Wishlist, product_id=product_id, user=request.user)
    wishlist_item.delete()
    return redirect('wishlist_view')

@login_required
def wishlist_view(request):
    if request.user.is_authenticated:
        # Retrieve the wishlist items for the logged-in user
        wishlist_items = Wishlist.objects.filter(user=request.user)
        # Extract the product from the wishlist items
        wishlist_product = [item.product for item in wishlist_items]
                # Get the user's profile
        return render(request, 'wishlist.html', {'wishlist_product': wishlist_product})
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



@login_required
def product_list(request):
    products = Product.objects.filter(user=request.user)
    return render(request, 'product_list.html', {'products': products})


@login_required
def order_placed(request):
    return render(request, 'order_placed.html')

@login_required
def order_details(request):
    return render(request, 'order_details.html')

# Display Stock Details
@login_required
def stock_details(request):
    user = request.user
    
    # Filter SizeStock objects based on the user
    size_stocks = SizeStock.objects.filter(product__user=user)
    
    # Function to check if stock is zero and create notification
    zero_stock_sizes = []
    for stock in size_stocks:
        if stock.stock_quantity == 0:
            zero_stock_sizes.append(stock)
            
            # Create a notification
            Notification.objects.create(
                recipient=user,
                message=f"{stock.product.brand_name} size- {stock.size} is out of stock.",
                timestamp=timezone.now()
            )

    context = {
        'size_stocks': size_stocks,
        'zero_stock_sizes': zero_stock_sizes,  # Pass the list of SizeStock objects with zero stock
    }

    return render(request, 'stock_details.html', context)


@login_required
def stock_details1(request):
    user = request.user
    
    # Filter SizeStock objects based on the user
    size_stocks = SizeStock.objects.filter(product__user=user)
    
    # Function to check if stock is zero and create notification
    zero_stock_sizes = []
    for stock in size_stocks:
        if stock.stock_quantity == 0:
            zero_stock_sizes.append(stock)
            
            # Create a notification
            Notification.objects.create(
                recipient=user,
                message=f"The stock for {stock.product.brand_name} - {stock.size} is out of stock.",
                timestamp=timezone.now()
            )

    context = {
        'size_stocks': size_stocks,
        'zero_stock_sizes': zero_stock_sizes,  # Pass the list of SizeStock objects with zero stock
    }

    return render(request, 'mdashboard2.html', context)


@login_required
def shipping_address(request):
    user = request.user

    if request.method == 'POST':
        # Extracting form data from the request
        name = request.POST.get('name')
        email = request.POST.get('email')
        phn1 = request.POST.get('phn1')
        phn2 = request.POST.get('phn2')
        address = request.POST.get('address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        district = request.POST.get('district')
        pin = request.POST.get('pin')
        land = request.POST.get('land')
        city = request.POST.get('city')
        # product_id = request.POST.get('product_id')
        user_id = request.POST.get('user_id')

        # Print or log the values to check if they are received correctly
        print(f"Name: {name}, Email: {email},  User ID: {user_id}")

        # Creating a ShippingAddress object and saving it to the database
        shipping_address_obj = ShippingAddress(
            name=name,
            email=email,
            phn1=phn1,
            phn2=phn2,
            address=address,
            country=country,
            state=state,
            district=district,
            pin=pin,
            land=land,
            city=city,
            # product=product,
            user=user,
        )
        shipping_address_obj.save()

        messages.success(request, 'Shipping address saved successfully.')
        return redirect('summery')  # Redirect to the order placed page or any other page

    return render(request, 'shippingaddress.html')



# new cart
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    selected_size = request.POST.get('selected-size', '1')  # Extract selected size from POST data
    print(selected_size)
    
    # Assuming CartItem has a 'size' field to store the selected size
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product, size=selected_size)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        
    return redirect('cart')




def remove_from_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = Cart.objects.get(user=request.user)
    try:
        cart_item = cart.cartitem_set.get(product=product)
        if cart_item.quantity >= 1:
             cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    
    return redirect('cart')

@login_required
def view_cart(request):
    cart = request.user.cart
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart.html', {'cart_items': cart_items})


def increase_cart_item(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.user.cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')


def decrease_cart_item(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart = request.user.cart
    
    try:
        cart_item = cart.cartitem_set.filter(product=product).first()
        
        if cart_item:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
    except ObjectDoesNotExist:
        pass

    return redirect('cart')




def fetch_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart = request.user.cart
        cart_count = CartItem.objects.filter(cart=cart).count()
    return JsonResponse({'cart_count': cart_count})


def get_cart_count(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart=request.user.cart)
        cart_count = cart_items.count()
    else:
        cart_count = 0
    return cart_count




@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        user = request.user
        cart = user.cart

        cart_items = CartItem.objects.filter(cart=cart)
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        try:
            order = Order.objects.create(user=user, total_amount=total_amount)
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    item_total=cart_item.product.price * cart_item.quantity
                )

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment_data = {
                'amount': int(total_amount * 100),
                'currency': 'INR',
                'receipt': f'order_{order.id}',
                'payment_capture': '1'
            }
            orderData = client.order.create(data=payment_data)
            order.payment_id = orderData['id']
            order.save()

            return JsonResponse({'order_id': orderData['id']})
        
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)
        
        
@login_required
def summery(request):
    user = request.user
    cart_items = CartItem.objects.filter(cart=request.user.cart)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    shipping_address = ShippingAddress.objects.filter(user=user).last()



    context = {

        'cart_items': cart_items,
        'total_amount': total_amount,
        'shipping_address': shipping_address,

    }
    return render(request, 'summery.html', context)



@csrf_exempt
def handle_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        razorpay_order_id = data.get('order_id')
        payment_id = data.get('payment_id')

        try:
            order = Order.objects.get(payment_id=razorpay_order_id)

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment = client.payment.fetch(payment_id)

            if payment['status'] == 'captured':
                order.payment_status = True
                order.save()        
                user = request.user
                user.cart.cartitem_set.all().delete()

                # for order_item in order.orderitem_set.all():
                #         product = order_item.product
                #         product.stock -= order_item.quantity
                #         product.save()


                data = {
                  'order_id': order.id,
                   'transID': order.payment_id,
            }
                return JsonResponse({'message': 'Payment successful', 'order_id': order.id, 'transID': order.payment_id})
            #     return JsonResponse({'message': 'Payment successful'})
            # else:
            #     return JsonResponse({'message': 'Payment failed'})

        except Order.DoesNotExist:
            return JsonResponse({'message': 'Invalid Order ID'})
        except Exception as e:

            print(str(e))
            return JsonResponse({'message': 'Server error, please try again later.'})
        
        
@login_required       
def order_complete(request):
    order_id = request.GET.get('order_id')
    transID = request.GET.get('payment_id')
    print("Order ID from GET parameters:", order_id)
    try:
   
        order = Order.objects.get(id=order_id, payment_status=True)
        print("Retrieved Order:", order)
        ordered_products = OrderItem.objects.filter(order_id=order.id)

        # subtotal = 0
        # for i in ordered_products: 
        #     subtotal += i.product.sale_price * i.quantity
        

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_id': order.id,
           'transID': transID,
        #    'subtotal': subtotal,
        }

        return render(request, 'order_complete.html', context)
    except Order.DoesNotExist:
        return redirect('summery')
    
# Main Project

# Add Agent
def generate_username(first_name, last_name):
    base_username = (first_name + last_name).lower()
    potential_username = base_username + ''.join(random.choices(string.ascii_letters, k=5)).lower()

    while User.objects.filter(username=potential_username).exists():
        potential_username = base_username + ''.join(random.choices(string.ascii_letters, k=5)).lower()

    return potential_username

def generate_password(name):
    # Use a simple password generation logic (you may want to implement a more secure approach)
    password = name.lower() + '123'
    return password


@login_required
def add_agent(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        password = generate_password(first_name)
        username = generate_username(first_name, last_name)

        if username and first_name and last_name and email and phone and password:

            if User.objects.filter(username=username).exists():
                return HttpResponseRedirect(reverse('add_agent') + '?alert=username_is_already_registered')

            elif User.objects.filter(email=email).exists():
                return HttpResponseRedirect(reverse('add_agent') + '?alert=email_is_already_registered')

            elif User.objects.filter(phone_no=phone).exists():
                return HttpResponseRedirect(reverse('add_agent') + '?alert=phone_no_is_already_registered')

            else:
                user = User(username=username, first_name=first_name, last_name=last_name, email=email, phone_no=phone)
                user.set_password(password)
                user.user_type = CustomUser.AGENT
                user.save()

                user_profile = UserProfile(user=user)
                user_profile.save()
                agent_profile = AgentProfile(user=user)
                agent_profile.save()

                # Send welcome email
                send_welcome_emaila(user.username,user.first_name,user.last_name,user.email,password)

                response = HttpResponseRedirect(reverse('add_agent') + '?alert=registered')
                response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
                response['Pragma'] = 'no-cache'
                response['Expires'] = '0'
                return response

    return render(request, 'add_agent.html')

def send_welcome_emaila(username,first_name,last_name,email,password):
    subject = 'Welcome to StepGuide'
    message = f"Hello {first_name},\n\n"
    message += f"Welcome to StepGuide,We are excited to have you join us!\n\n"
    
    # Retrieve the associated subscription object # Assuming sub_type is a ManyToMany field

    # message += f"You login credentials are {username} plan, which is valid for {password}.\n\n"
    message += f"You login credentials are\nusername: {username}\nPassword: {password} \n\n"

    
    # message += "Please feel free to contact the property owner for more information or to schedule a viewing of the property.\n\n"
    # message += "Thank you for choosing FindMyNest. We wish you the best in your property search!\n\n"
    message += "Warm regards,\nThe StepGuide Team\n\n"
    
    from_email = 'stepguide0@gmail.com'  # Replace with your actual email
    recipient_list = [email]

    # Create a PDF invoice and attach it to the email

    # Send the email
    send_mail(subject, message, from_email, recipient_list)
    
# nxt



@login_required 
def my_orders(request):
    # Retrieve orders with payment_status set to True for the current user, ordered by date created (most recent first)
    orders = Order.objects.filter(user=request.user, payment_status=True).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})


@login_required
def rating0(request, product_id):
    products = get_object_or_404(Product,id=product_id)
    orders = Order.objects.filter(user=request.user, payment_status=True).order_by('-created_at')
    ratings = Rating.objects.filter(products=products)

    context = {
        'products': products,
        'ratings': ratings,
        'orders': orders,
    }

    return render(request, 'rating.html', context)


# Rating
@login_required
def rating(request, product_id):
    if request.method == 'POST':
        user = request.user
        value = int(request.POST['rating'])
        comment = request.POST.get('comment', '')
        product=Product.objects.get(pk=product_id)

        rating, created = Rating.objects.get_or_create(user=user, products=product, defaults={'value': value, 'comment': comment})

        if not created:
            rating.value = value
            rating.comment = comment
            rating.save()

        return redirect('rating0', product_id=product_id)
    else:
        return redirect('index')



# Agent Dashboard
@login_required
def adashboard(request):
    user=request.user
    if request.user.is_authenticated:
        if user.user_type == CustomUser.ADMIN and not request.path == reverse('dashboard1'):
            return redirect(reverse('dashboard1'))
        elif user.user_type == CustomUser.CLIENT and not request.path == reverse('index'):
            return redirect(reverse('index'))
        elif user.user_type == CustomUser.MERCHANT and not request.path == reverse('mdashboard2'):
            return redirect(reverse('mdashboard2'))  
        elif user.user_type == CustomUser.AGENT and not request.path == reverse('adashboard'):
            return redirect(reverse('adashboard')) 
    else:
        return redirect(reverse('index'))
    merchant_products = Product.objects.filter(user=request.user)
    product_count = merchant_products.count()
    new_arrival_count = NewArrival.objects.filter(user=request.user).count()
    return_request_count = ProductReturn.objects.filter(user=request.user).count()
    approved_return_count = ProductReturn.objects.filter(agent=request.user, status='Accepted').count()
    rejected_return_count = ProductReturn.objects.filter(agent=request.user, status='Rejected').count()
    return render(request,'adashboard.html',{'merchant_products': merchant_products, 'product_count': product_count, 'new_arrival_count': new_arrival_count, 'return_request_count': return_request_count, 'approved_return_count': approved_return_count, 'rejected_return_count': rejected_return_count})


# Agent Stock View
@login_required
def astock_details(request):
    # Retrieve all SizeStock objects
    size_stocks = SizeStock.objects.all()

    context = {
        'size_stocks': size_stocks,
    }

    return render(request, 'astock_details.html', context)



# Chat
from StepGuideApp.models import Thread
@login_required
def messages_page(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads
    }
    return render(request, 'messages.html', context)


# Agent Edit Profile
@login_required
def agent_profile(request):
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

        return redirect('agent_profile')
    context = {
        'user': user,
        'user_profile': user_profile,
    }
    return render(request, 'agent_profile.html',context)


# Comparison
@login_required
def add_to_compare(request, product_id):
    # Retrieve the property object
    product_obj = get_object_or_404(Product, pk=product_id)

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get or create CompareProperty object for the user
        compare_product, created = CompareProduct.objects.get_or_create(user=request.user)

        # Check if the property is already in the compare list
        if product_obj in compare_product.Product.all():
            messages.error(request, "This property is already in your compare list.")
        elif compare_product.Product.count() >= 4:
            messages.error(request, "You can only compare up to 4 properties.")
        else:
            # Add the property to the compare list
            compare_product.Product.add(product_obj)
            messages.success(request, "Property added to compare list successfully.")
    else:
        messages.error(request, "You need to be logged in to add properties to compare list.")

    return redirect('purchase', product_id=product_id)

@login_required
def compare_product(request):
    # Get the CompareProperty objects for the logged-in user
    compare_product = CompareProduct.objects.filter(user=request.user)

    context = {'compare_product': compare_product}

    return render(request, 'compare_product.html', context)

@login_required
def remove_product(request, product_id):
    try:
        user = request.user
        compare_product = CompareProduct.objects.get(user=user)
        product_to_remove = compare_product.Product.get(id=product_id)
        compare_product.Product.remove(product_to_remove)
        return redirect(reverse('compare_product'))  # Redirect to another view after removal
    except CompareProduct.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'CompareProduct not found'})
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found'})
    
    
# update Product
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['brand_name', 'category', 'subcategory', 'product_description', 'material_description', 'male', 'female', 'price', 'thumbnail'] 


@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to product list page after successful update
    else:
        form = ProductForm(instance=product)
    return render(request, 'update_product.html', {'form': form})


@login_required
def disable_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.status = False
    product.save()
    return redirect('product_list')  # Redirect to product list page after disabling the product


@login_required
def enable_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.status = True
    product.save()
    return redirect('product_list') 

@login_required
def clear_all_notifications(request):
    if request.method == 'POST':
        Notification.objects.filter(recipient=request.user).delete()
    return redirect('mdashboard2')

@login_required
def add_new_arrival(request):
    if request.method == 'POST':
        form = NewArrivalForm(request.POST, request.FILES)
        if form.is_valid():
            new_arrival = form.save(commit=False)
            new_arrival.user = request.user
            new_arrival.save()
            return redirect('new_arrival_list')  # Redirect to the merchant dashboard or any other appropriate page
    else:
        form = NewArrivalForm()
    return render(request, 'add_new_arrival.html', {'form': form})


@login_required
def new_arrival_list(request):
    new_arrivals = NewArrival.objects.filter(user=request.user)
    return render(request, 'new_arrival_list.html', {'new_arrivals': new_arrivals})


@login_required
def new_arrival_edit(request, pk):
    new_arrival = get_object_or_404(NewArrival, pk=pk)
    if request.method == 'POST':
        form = NewArrivalForm(request.POST, instance=new_arrival)
        if form.is_valid():
            form.save()
            return redirect('new_arrival_list')
    else:
        form = NewArrivalForm(instance=new_arrival)
    return render(request, 'new_arrival_edit.html', {'form': form})


@login_required
def new_arrival_delete(request, pk):
    new_arrival = get_object_or_404(NewArrival, pk=pk)
    if request.method == 'POST':
        new_arrival.delete()
        return redirect('new_arrival_list')
    return render(request, 'new_arrival_delete.html', {'new_arrival': new_arrival})


@login_required
def view_arrival(request):
    new_arrivals = NewArrival.objects.all()
    return render(request, 'view_arrival.html', {'new_arrivals': new_arrivals})


# Retun Product
@login_required
def return_product(request):
    if request.method == 'POST':
        form = ProductReturnForm(request.POST, request.FILES)
        if form.is_valid():
            product_return = form.save(commit=False)
            product_return.user = request.user
            product_return.save()
            return redirect('mdashboard2')  # Redirect to the merchant dashboard
    else:
        form = ProductReturnForm()
    return render(request, 'return_product.html', {'form': form})


@login_required
def view_returns(request):
    if request.method == 'POST':
        product_return = ProductReturn.objects.get(pk=request.POST['product_return_id'])
        if 'approve' in request.POST:
            product_return.status = 'Accepted'
            product_return.agent = request.user
        elif 'reject' in request.POST:
            product_return.status = 'Rejected'
        product_return.save()
        return redirect('view_returns')  # Redirect to the agent dashboard

    returns = ProductReturn.objects.filter(agent=request.user)
    return render(request, 'view_returns.html', {'returns': returns})


@login_required
def returned_product_list(request):
    # Filter returned products based on the current user's ID
    returned_products = ProductReturn.objects.filter(user=request.user)
    return render(request, 'returned_product_list.html', {'returned_products': returned_products})
