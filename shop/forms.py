from django import forms
from .models import Brand, Product

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand name'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['brand', 'name', 'buying_price', 'selling_price']
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product name'}),
            'buying_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
