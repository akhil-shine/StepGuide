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
    phone_no = models.CharField(max_length=12,unique=True)
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
            return self.user.username
        else:
            return "UserProfile with no associated user"