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
    profile_pic=models.FileField(upload_to='profile_pic/',blank=True,null=True)
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
    stock_16_18 = models.PositiveIntegerField(default=0)
    stock_20_24 = models.PositiveIntegerField(default=0)
    stock_25_29 = models.PositiveIntegerField(default=0)
    stock_30_35 = models.PositiveIntegerField(default=0)
    
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
    
    def str(self):
        # return self.book.title
        return f"cart details {self.user.email}: {self.product.brand_name}"
    
