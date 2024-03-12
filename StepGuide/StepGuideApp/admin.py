from django.contrib import admin
from .models import CustomUser,UserProfile,Category,Subcategory,Product,Image,Wishlist,BookCart,SizeStock,ShippingAddress,Cart,CartItem,Order,OrderItem,AgentProfile,NewArrival,ProductReturn
from .models import Thread, ChatMessage



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
admin.site.register(AgentProfile)
admin.site.register(NewArrival)
admin.site.register(ProductReturn)





# Chat
admin.site.register(ChatMessage)

class ChatMessage(admin.TabularInline):
    model = ChatMessage


# class ThreadForm(forms.ModelForm):
#     def clean(self):
#         """
#         This is the function that can be used to
#         validate your model data from admin
#         """
#         super(ThreadForm, self).clean()
#         first_person = self.cleaned_data.get('first_person')
#         second_person = self.cleaned_data.get('second_person')
#
#         lookup1 = Q(first_person=first_person) & Q(second_person=second_person)
#         lookup2 = Q(first_person=second_person) & Q(second_person=first_person)
#         lookup = Q(lookup1 | lookup2)
#         qs = Thread.objects.filter(lookup)
#         if qs.exists():
#             raise ValidationError(f'Thread between {first_person} and {second_person} already exists.')
#

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread


admin.site.register(Thread, ThreadAdmin)
