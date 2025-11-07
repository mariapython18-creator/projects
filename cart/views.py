from django.shortcuts import render,redirect

from django.views import View

from shop.models import Products

from .forms import Order_form
from .models import Products, Cart, Order_items,Order
import razorpay
from django.contrib.auth.models import User
from django.contrib.auth import login

# Create your views here.
class Cart_view(View):
    def get(self,request,i):
        p=Products.objects.get(id=i)
        u=request.user
        try:
            c=Cart.objects.get(user=u,product=p)
            c.quantity+=1
            c.save()
        except:
               c = Cart.objects.create(user=u, product=p,quantity=1)
               c.save()
        return redirect('cart:my_cart')
class Mycart_view(View):
    def get(self,request):
        u=request.user
        total=0
        c=Cart.objects.filter(user=u)
        for i in c:
            total+=i.quantity*i.product.price
        context={'cart':c,'total':total}
        return render(request,'add_cart.html',context)
class Decrement_view(View):
    def get(self,request,i):
        p=Products.objects.get(id=i)
        u=request.user
        try:
            c=Cart.objects.get(user=u,product=p)
            if c.quantity>1:
                c.quantity-=1
                c.save()
            else:
                c.delete()

        except:
            pass
        return redirect('cart:my_cart')
class Remove_view(View):
    def get(self,request,i):
        p=Products.objects.get(id=i)
        u=request.user
        try:
            c=Cart.objects.get(user=u,product=p)
            c.delete()
        except:
               pass
        return redirect('cart:my_cart')
def checkout(c):
    stock=True
    for i in c:
        if i.product.stock<i.quantity:
            stock=False
            break
    return stock

class Checkout_view(View):
    def get(self, request):
        form = Order_form()
        context = {'form': form}
        return render(request, 'checkout.html', context)

    def post(self, request):
        print(request.POST)
        u = request.user
        c = Cart.objects.filter(user=u)
        stock = checkout(c)
        if stock:
            form = Order_form(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = u
                obj.save()
                total = 0
                for i in c:
                    total += i.product.price * i.quantity
                for i in c:
                    o=Order_items.objects.create(order=obj,product=i.product,quantity=i.quantity)
                    o.save()

                if obj.payment_method.upper() == "ONLINE":
                    client = razorpay.Client(auth=('rzp_test_RKKzHKHvxWqtrB', 'R0VT15Y2OTfNrJtsKPnzsSN4'))
                    response_payment = client.order.create(dict(
                        amount=total * 100,
                        currency="INR",
                    ))
                    print(response_payment)
                    obj.order_id = response_payment["id"]
                    obj.amount = total
                    obj.save()
                    context = {'payment': response_payment}
                    return render(request, 'payment.html', context)

                elif obj.payment_method.upper() == "COD":
                    is_orderd=True
                    obj.amount=total
                    obj.save()
                    items=Order_items.objects.filter(order=obj)
                    for i in items:
                        i.product.stock-=i.quantity
                        i.product.save()
                    c.delete()
                    return render(request,"success.html")

                else:
                    return redirect('cart:my_cart')
            else:
                return render(request, 'checkout.html', {"form": form, "error": "Out of stock"})  #
        else:
            return render(request, 'checkout.html', {"form": form})
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
@method_decorator(csrf_exempt, name="dispatch")
class Payment_success(View):
    def post(self,request,i):
        u=User.objects.get(username=i)
        login(request,u)
        response=request.POST
        print(response)
        id=response['razorpay_order_id']
        o=Order.objects.get(order_id=id)
        print(o)
        o.is_orderd = True
        o.save()
        items = Order_items.objects.filter(order=o)
        for i in items:
            i.product.stock -= i.quantity
            i.product.save()
        c=Cart.objects.filter(user=request.user)
        c.delete()
        return render(request,"payment_success.html")
class Ordersummary(View):
    def get(self,request):
        u=request.user
        c=Order.objects.filter(user=u,is_ordered=True)
        context={'order':c}
        return render(request,"summary.html",context)
