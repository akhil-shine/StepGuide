from django.contrib import admin
from .models import CustomUser,UserProfile,Category,Subcategory,Product,Image

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(Image)