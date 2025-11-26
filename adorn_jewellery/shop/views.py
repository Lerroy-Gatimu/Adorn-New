# adorn_jewellery/shop/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import json
import sys

# ─── FIX UnicodeEncodeError on Windows (MUST stay at the very top) ───
if sys.platform.startswith('win'):
    import smtplib
    from email.message import EmailMessage

    def _utf8_sendmail(self, from_addr, to_addrs, msg, mail_options=(), rcpt_options=()):
        if isinstance(msg, EmailMessage):
            msg_str = msg.as_string()
        else:
            msg_str = msg if isinstance(msg, str) else str(msg)
        msg_bytes = msg_str.encode('utf-8', errors='replace')
        return self._original_sendmail(from_addr, to_addrs, msg_bytes, mail_options, rcpt_options)

    if not hasattr(smtplib.SMTP, '_original_sendmail'):
        smtplib.SMTP._original_sendmail = smtplib.SMTP.sendmail
        smtplib.SMTP.sendmail = _utf8_sendmail

from .models import Product, Category, Order, OrderItem, ContactMessage, CartItem, WishlistItem
from .forms import SignUpForm


# ────────────────────────────────
# CART & WISHLIST API
# ────────────────────────────────
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
        if not created:
            wishlist_item.delete()

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


# ────────────────────────────────
# MAIN VIEWS
# ────────────────────────────────
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

        context = {
            'order': order,
            'items': order.items.all(),
            'customer_name': f"{order.first_name} {order.last_name}",
        }

        # Customer Email
        html_customer = render_to_string('emails/order_confirmation_customer.html', context)
        text_customer = strip_tags(html_customer)
        send_mail(
            subject=f"Your Order #{order.order_number} is Confirmed!",
            message=text_customer,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.email],
            html_message=html_customer,
            fail_silently=False,
        )

        # Admin Email
        html_admin = render_to_string('emails/order_notification_admin.html', context)
        text_admin = strip_tags(html_admin)
        send_mail(
            subject=f"NEW ORDER #{order.order_number} – KES {order.total_amount:,}",
            message=text_admin,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=html_admin,
            fail_silently=False,
        )

        request.user.cart_items.all().delete()
        messages.success(request, "Order placed successfully! Check your email.")
        return render(request, 'shop/order_confirmation.html', {'order': order})

    return render(request, 'shop/checkout.html')


@login_required
def my_account(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/my_account.html', {'orders': orders})


# ────────────────────────────────
# AUTH & CONTACT
# ────────────────────────────────
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
            messages.success(request, "Account created! Welcome to Adorn Jewellery.")
            return redirect('shop:home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('shop:home')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject') or "No Subject"
        message = request.POST.get('message')

        ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)

        context = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
        }

        html_message = render_to_string('emails/contact_message.html', context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject=f"New Message from {name}: {subject}",
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=html_message,
            fail_silently=False,
        )

        messages.success(request, "Thank you! Your message has been sent. We'll reply soon.")
        return redirect('shop:contact')
    
    return render(request, 'shop/contact.html')


def why_choose_us(request):
    return render(request, 'shop/why_choose_us.html')