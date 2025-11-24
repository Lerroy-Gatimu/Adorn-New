from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('checkout/', views.checkout, name='checkout'),
    path('my-account/', views.my_account, name='my_account'),
    path('contact/', views.contact, name='contact'),
    path('why-choose-us/', views.why_choose_us, name='why_choose_us'),
]
