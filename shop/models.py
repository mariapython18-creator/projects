from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='categories')

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='products')
    price=models.IntegerField(default=0)
    stock=models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)  # one time
    updated = models.DateField(auto_now=True)      # each time we update
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    def __str__(self):
        return self.name
class Register(models.Model):
    email = models.EmailField(unique=True, blank=False, null=False)
from django.utils import timezone

# Assuming you already have CustomUser and Product models defined

