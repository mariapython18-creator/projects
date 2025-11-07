from django.contrib import admin
from .models import Cart,Order,Order_items

# Register your models here.
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Order_items)