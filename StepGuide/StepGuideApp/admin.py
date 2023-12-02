from django.contrib import admin
from .models import CustomUser,UserProfile,Category,Subcategory,Product,Image,Wishlist,BookCart,SizeStock,ShippingAddress,Cart,CartItem,Order,OrderItem

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Wishlist)
admin.site.register(BookCart)
admin.site.register(SizeStock)
admin.site.register(ShippingAddress)


admin.site.register(Cart)
admin.site.register(CartItem)

admin.site.register(Order)
admin.site.register(OrderItem)