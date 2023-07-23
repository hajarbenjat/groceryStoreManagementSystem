# forms.py

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity']

class SaleForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity_sold = forms.IntegerField()
