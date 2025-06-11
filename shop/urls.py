from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.home, name='home'),
    path('add-brand/', views.add_brand, name='add_brand'),
    path('add-product/', views.add_product, name='add_product'),
    path('brand/<int:brand_id>/', views.brand_detail, name='brand_detail'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.showcart, name='showcart'),
    path('print-bill/', views.print_bill, name='print_bill'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('sales/', views.sales_history, name='sales_history'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),
]
