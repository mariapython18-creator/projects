"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from shop import views

app_name='shop'

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('category',views.Category_view.as_view(),name='category'),
    path('products/<int:i>',views.Products_view.as_view(),name='products'),
    path('details/<int:i>',views.Details.as_view(),name='details'),
    path('register',views.Register_view.as_view(),name='register'),
    path('login/',views.Login_view.as_view(),name='login'),
    path('logout/',views.Logout_view.as_view(),name='logout'),
    path('addcategory',views.Add_category.as_view(),name='addcategory'),
    path('addproduct',views.Add_product.as_view(),name='addproduct'),
    path('addstock/<int:i>',views.Add_stock.as_view(),name='addstock'),
# Password Reset
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    # Password Change (for logged-in users)
    path('password-change/',
         auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),

    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),
]

