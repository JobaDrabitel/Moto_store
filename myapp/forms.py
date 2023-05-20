from myapp.models import Product, ShippingMethod, PaymentMethod
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms


class OrderForm(forms.Form):
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    shipping_method = forms.ModelChoiceField(queryset=ShippingMethod.objects.all())
    payment_method = forms.ModelChoiceField(queryset=PaymentMethod.objects.all())


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'lastname', 'firstname', 'email', 'phone', 'address', 'image']


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'lastname', 'firstname', 'email', 'password', 'phone', 'address']


class LoginForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'description', 'price', 'imageurl')
