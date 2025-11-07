from django.shortcuts import render,redirect
from django.views import View
from .models import Category,Products
from .forms import Register_form, Login_form, Addcategory_form,Addproduct_form,Add_stock_form
from django.contrib.auth import authenticate, login,logout


# Create your views here.
class Category_view(View):
    def get(self,request):
        c=Category.objects.all()
        context={'category':c}
        return render(request,'category.html',context)
class Login_view(View):
    def get(self,request):
        form=Login_form()
        context={'form':form}
        return render(request,'login.html',context)
    def post(self,request):
        form=Login_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                  login(request, user)
                  return redirect('shop:category')
            else:
                 return render(request, "login.html", {"form": form, "error": "Invalid username or password"})
        else:
             return render(request, "login.html", {"form": form})


class Products_view(View):
    def get(self, request, i):
        # Get one category by ID
        c = Category.objects.get(id=i)

        # Pass that category to template
        return render(request, 'products.html', {'category': c})
class Details(View):
    def get(self,request,i):
        p=Products.objects.get(id=i)
        context={'products':p}
        return render(request,'details.html',context)
class Register_view(View):
    def get(self,request):
        form=Register_form()
        context={'form':form}
        return render(request,'register.html',context)
    def post(self,request):
        form=Register_form(request.POST)
        if form.is_valid():
            form.save()

            return redirect("login")
        else:
            return render(request, "register.html", {"form": form})

class Add_category(View):
    def get(self, request):
        form = Addcategory_form()
        context = {'form': form}
        return render(request, 'add_category.html', context)

    def post(self, request):
        form = Addcategory_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shop:category')
        else:
            context = {'form': form}  # show form errors
            return render(request, 'add_category.html', context)

class Add_product(View):
    def get(self,request):
            form = Addproduct_form()
            context = {'form': form}
            return render(request, 'add_product.html', context)
    def post(self,request):
        form=Addproduct_form(request.POST,request.FILES)
        if form.is_valid():
             form.save()
             return redirect('shop:category')
class Add_stock(View):
        def get(self, request, i):
            p = Products.objects.get(id=i)
            form = Add_stock_form(instance=p)
            return render(request, 'add_stock.html', {'form': form})

        def post(self, request, i):
            p = Products.objects.get(id=i)
            form = Add_stock_form(request.POST, instance=p)
            if form.is_valid():
                form.save()
                return redirect('shop:category')
            # If invalid, re-render form
            return render(request, 'add_stock.html', {'form': form})

class Logout_view(View):
    def get(self, request):
        logout(request)  # Logs out the current user
        return redirect('shop:category')  # Redirect after logout