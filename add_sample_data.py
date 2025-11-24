import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adorn_jewellery.settings')
django.setup()

from adorn_jewellery.shop.models import Category, Product

categories_data = [
    {'name': 'Necklaces', 'description': 'Elegant necklaces for every occasion'},
    {'name': 'Earrings', 'description': 'Beautiful earrings to complement your style'},
    {'name': 'Bracelets', 'description': 'Stunning bracelets that add elegance'},
    {'name': 'Rings', 'description': 'Exquisite rings for special moments'},
]

products_data = [
    {
        'name': 'Diamond Pendant Necklace',
        'category': 'Necklaces',
        'description': 'A stunning diamond pendant necklace that adds elegance to any outfit. Features a brilliant-cut diamond set in 18k gold.',
        'price': 299.99,
        'original_price': 399.99,
        'stock': 15,
        'is_featured': True,
    },
    {
        'name': 'Pearl Drop Earrings',
        'category': 'Earrings',
        'description': 'Classic pearl drop earrings perfect for formal occasions. Made with freshwater pearls and sterling silver.',
        'price': 89.99,
        'original_price': 129.99,
        'stock': 25,
        'is_featured': True,
    },
    {
        'name': 'Gold Chain Bracelet',
        'category': 'Bracelets',
        'description': 'Delicate gold chain bracelet that adds a touch of sophistication. Adjustable length for perfect fit.',
        'price': 149.99,
        'stock': 20,
        'is_featured': True,
    },
    {
        'name': 'Sapphire Engagement Ring',
        'category': 'Rings',
        'description': 'Beautiful sapphire engagement ring surrounded by diamonds. A timeless symbol of love and commitment.',
        'price': 1299.99,
        'original_price': 1599.99,
        'stock': 5,
        'is_featured': True,
    },
    {
        'name': 'Silver Hoop Earrings',
        'category': 'Earrings',
        'description': 'Modern silver hoop earrings perfect for everyday wear. Lightweight and comfortable.',
        'price': 49.99,
        'stock': 30,
        'is_featured': True,
    },
    {
        'name': 'Rose Gold Heart Necklace',
        'category': 'Necklaces',
        'description': 'Romantic rose gold heart necklace, perfect gift for loved ones. Comes with a beautiful gift box.',
        'price': 79.99,
        'stock': 40,
        'is_featured': True,
    },
    {
        'name': 'Gemstone Tennis Bracelet',
        'category': 'Bracelets',
        'description': 'Elegant tennis bracelet featuring alternating gemstones. Perfect for special occasions.',
        'price': 249.99,
        'original_price': 349.99,
        'stock': 12,
    },
    {
        'name': 'Gold Band Ring',
        'category': 'Rings',
        'description': 'Simple yet elegant gold band ring. Perfect for stacking or wearing alone.',
        'price': 199.99,
        'stock': 18,
    },
    {
        'name': 'Crystal Chandelier Earrings',
        'category': 'Earrings',
        'description': 'Glamorous crystal chandelier earrings that catch the light beautifully. Perfect for evening wear.',
        'price': 119.99,
        'stock': 15,
    },
    {
        'name': 'Layered Chain Necklace',
        'category': 'Necklaces',
        'description': 'Trendy layered chain necklace with multiple strands. On-trend and versatile.',
        'price': 69.99,
        'stock': 35,
    },
]

for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description']}
    )
    if created:
        print(f'Created category: {category.name}')

for prod_data in products_data:
    category = Category.objects.get(name=prod_data['category'])
    product, created = Product.objects.get_or_create(
        name=prod_data['name'],
        defaults={
            'category': category,
            'description': prod_data['description'],
            'price': prod_data['price'],
            'original_price': prod_data.get('original_price'),
            'stock': prod_data['stock'],
            'is_featured': prod_data.get('is_featured', False),
        }
    )
    if created:
        print(f'Created product: {product.name}')

print('\nSample data added successfully!')
