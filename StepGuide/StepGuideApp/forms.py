from django import forms
from .models import CustomUser, NewArrival
from .models import ProductReturn

class NewArrivalForm(forms.ModelForm):
    class Meta:
        model = NewArrival
        fields = ['product_name', 'image', 'given_price', 'mrp', 'size_available']
        
class ProductReturnForm(forms.ModelForm):
    agent = forms.ModelChoiceField(queryset=CustomUser.objects.filter(user_type=CustomUser.AGENT))

    class Meta:
        model = ProductReturn
        fields = ['agent', 'product_name', 'image', 'reason']
