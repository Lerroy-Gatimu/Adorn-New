# adorn_jewellery/shop/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
import json

from .models import Product, Category, Order, OrderItem, ContactMessage
from .forms import SignUpForm

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

# ── CART API ──
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return JsonResponse({'success': True, 'cart_count': request.user.cart_items.count()})

    return JsonResponse({'success': False})


@login_required
def get_cart_count(request):
    count = request.user.cart_items.count() if request.user.is_authenticated else 0
    return JsonResponse({'cart_count': count})


@login_required
def get_cart_items(request):
    items = request.user.cart_items.select_related('product').all()
    data = [{
        'id': item.product.id,
        'name': item.product.name,
        'price': float(item.product.price),
        'quantity': item.quantity,
        'image': item.product.image.url if item.product.image else '',
        'slug': item.product.slug
    } for item in items]
    return JsonResponse({'items': data})


# ── WISHLIST API ──
@login_required
def add_to_wishlist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        wishlist_item, created = WishlistItem.objects.get_or_create(
            user=request.user,
            product=product
        )
        action = "added" if created else "removed"
        wishlist_item.delete() if not created else None

        return JsonResponse({
            'success': True,
            'action': action,
            'wishlist_count': request.user.wishlist_items.count()
        })

    return JsonResponse({'success': False})


@login_required
def get_wishlist_count(request):
    count = request.user.wishlist_items.count() if request.user.is_authenticated else 0
    return JsonResponse({'wishlist_count': count})


def home(request):
    featured_products = Product.objects.filter(is_featured=True, is_available=True)[:6]
    categories = Category.objects.all()
    return render(request, 'shop/home.html', {
        'featured_products': featured_products,
        'categories': categories,
    })


def shop(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    
    # Filtering & sorting (unchanged)
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    sort_by = request.GET.get('sort')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    
    return render(request, 'shop/shop.html', {
        'products': products,
        'categories': categories,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related_products = Product.objects.filter(
        category=product.category, 
        is_available=True
    ).exclude(id=product.id)[:4]
    
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })


# PROTECTED VIEWS — require login
@login_required
def cart(request):
    return render(request, 'shop/cart.html')

@login_required
def wishlist(request):
    return render(request, 'shop/wishlist.html')

@login_required
def checkout(request):
    if request.method == 'POST':
        cart_data = json.loads(request.POST.get('cart_data', '[]'))
        if not request.user.is_authenticated:
            return redirect('shop:login')

        order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            postal_code=request.POST.get('postal_code'),
            country=request.POST.get('country'),
            total_amount=request.POST.get('total_amount'),
            notes=request.POST.get('notes', ''),
        )
        
        for item in cart_data:
            product = Product.objects.get(id=item['id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=product.price
            )
            product.stock -= item['quantity']
            product.save()
        
        return render(request, 'shop/order_confirmation.html', {'order': order})
    
    return render(request, 'shop/checkout.html')

@login_required
def my_account(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/my_account.html', {'orders': orders})


# AUTH VIEWS
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next', 'shop:home')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})


def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully! Welcome to Adorn Jewellery.")
            return redirect('shop:home')
    else:
        form = SignUpForm()
    
    return render(request, 'registration/signup.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('shop:home')


def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('shop:contact')
    
    return render(request, 'shop/contact.html')


def why_choose_us(request):
    return render(request, 'shop/why_choose_us.html')