from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


class CustomUser(AbstractUser):
    CLIENT = 1
    ADMIN = 2
    MERCHANT = 3

    ROLE_CHOICE = (
        (CLIENT, 'Client'),
        (ADMIN,'Admin'),
        (MERCHANT,'Merchant')
    )


    username = models.CharField(max_length=100,unique=True)
    first_name = models.CharField(max_length=100,)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,unique=True)
    phone_no = models.CharField(max_length=12)
    user_type = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)
   
    object = UserManager() 
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_no','email','first_name','last_name','password']

    def _str_(self):
        return self.first_name
    
    
class UserProfile(models.Model):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    profile_pic=models.FileField(upload_to='profile/',default="")
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def _str_(self):
        if self.user:
            return self.user
        else:
            return "UserProfile with no associated user"
        
# add categoryy
class Category(models.Model):
    category_name = models.CharField(max_length=30, default='Unknown')
    # category_image = models.ImageField(upload_to='pic', default='')
    descriptioncat = models.CharField(max_length=500, null=False, blank=False, default="Default category description")
    status=models.BooleanField(default=False)

    def _str_(self):
        return self.category_name
class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=500, null=False, blank=False, default="Default subcategory description")
    status = models.BooleanField(default=False)

    def _str_(self):
        return self.name
    
# add product in merchant
class Product(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True,related_name="user")
    brand_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)  # You may want to create a separate Subcategory model.
    # quantity = models.PositiveIntegerField()
    product_description = models.TextField()
    material_description = models.TextField()
    male = models.BooleanField(default=False)
    female = models.BooleanField(default=False)
    thumbnail = models.FileField(upload_to='thumbnail/',default="")

    
    # Size-specific stock fields
    stock_for_child_1_3 = models.PositiveIntegerField(default=0)
    stock_4_8 = models.PositiveIntegerField(default=0)
    stock_9_12 = models.PositiveIntegerField(default=0)
    
     # Calculate total stock as the sum of individual stock fields
    total_stock = models.PositiveIntegerField(default=0) # Make it non-editable

    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_16_19 = models.DecimalField(max_digits=10, decimal_places=2)
    
    
    # Other fields you may want to add
    
    def __str__(self):
        return self.brand_name
    
class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='product_images/', blank=True)  

    def _str_(self):
        return f"Image for {self.product.brand_name}"
    
    
# Total Stock Details
class SizeStock(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size = models.CharField(max_length=50)
    stock_quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.brand_name} - {self.size}"
    
    
# wishlist
class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def str(self):
        return f'{self.user.username} - {self.product.brand_name}'
    
# Cart
class BookCart(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    status=models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=1, null=True)
    size = models.PositiveIntegerField(default=1, null=True)
    
    
    def str(self):
        # return self.book.title
        return f"cart details {self.user.email}: {self.product.brand_name}"
    


# shipping Address
class ShippingAddress(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    phn1 = models.CharField(max_length=15)
    phn2 = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    pin = models.CharField(max_length=10)
    land = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    # quantity = models.PositiveIntegerField()
    # price = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    # total_price = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    # size = models.PositiveIntegerField(default=1, null=True)
    def __str__(self):
        return self.name
    
# Payment
# class Payment(models.Model): 
#     class PaymentStatusChoices(models.TextChoices):
#         PENDING = 'pending', 'Pending'
#         SUCCESSFUL = 'successful', 'Successful'
#         FAILED = 'failed', 'Failed'
        
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link the payment to a user
#     razorpay_order_id = models.CharField(max_length=255)  # Razorpay order ID
#     payment_id = models.CharField(max_length=255)  # Razorpay payment ID
#     amount = models.DecimalField(max_digits=8, decimal_places=2)  # Amount paid
#     currency = models.CharField(max_length=3)  # Currency code (e.g., "INR")
#     timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of the payment
#     payment_status = models.CharField(max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)

#     def str(self):
#         return f"Order for {self.user.username}"

#     class Meta:
#         ordering = ['-timestamp']

# #Update Status not implemented
#     def update_status(self):
#         # Calculate the time difference in minutes
#         time_difference = (timezone.now() - self.timestamp).total_seconds() / 60

#         if self.payment_status == self.PaymentStatusChoices.PENDING and time_difference > 1:
#             # Update the status to "Failed"
#             self.payment_status = self.PaymentStatusChoices.FAILED
#             self.save()



class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.PositiveIntegerField(default=1, null=True)


    def __str__(self):
        return f"{self.quantity} x {self.product.brand_name}"

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart for {self.user.username}"

# User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
# User.cart = property(lambda u: Cart.objects.get_or_create(user=u)[0])




class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.PositiveIntegerField(default=1, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.brand_name} in Order {self.order.id}"