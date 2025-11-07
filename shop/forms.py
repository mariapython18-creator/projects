from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from.models import Category,Products
from shop.models import Category


class Register_form(UserCreationForm):
    class Meta:
      model =User
      fields =['username' ,'password1','password2' ,'email']


class Login_form(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
class Addcategory_form(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'
class Addproduct_form(forms.ModelForm):
    class Meta:
        model=Products
        fields=['name','description','image','price','stock','category']
class Add_stock_form(forms.ModelForm):
    class Meta:
        model=Products
        fields=['stock']

