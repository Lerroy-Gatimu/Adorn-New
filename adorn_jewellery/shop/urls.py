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

    # Authentication
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),

    path('api/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('api/add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('api/cart-count/', views.get_cart_count, name='get_cart_count'),
    path('api/wishlist-count/', views.get_wishlist_count, name='get_wishlist_count'),
    path('api/cart-items/', views.get_cart_items, name='get_cart_items'),
]
