# Adorn Jewellery - Django E-commerce Website

## Overview
Adorn Jewellery is a fully functional Django-based e-commerce website specializing in elegant, affordable, and unique jewelry. The website features a clean, sophisticated design with a gold and black color palette that reflects the luxury jewelry brand.

**Motto:** Distinctively Elegant, Affordable, Unique

## Project Structure

### Django Apps
- **shop**: Main e-commerce functionality (products, orders, cart, wishlist)
- **pages**: Additional static pages

### Key Features
1. **Home Page**: Hero section, category browsing, featured products, brand story
2. **Shop Page**: Product grid with filtering by category and price, sorting options
3. **Product Detail Pages**: Full product information, quantity selector, related products
4. **Shopping Cart**: Dynamic cart with localStorage persistence, quantity adjustment
5. **Wishlist**: Save favorite items with localStorage persistence
6. **Checkout**: Complete order form with shipping information
7. **Contact Us**: Contact form with business information
8. **Why Choose Us**: Brand values and unique selling points
9. **My Account**: Order history and account dashboard

### Technology Stack
- **Backend**: Django 5.2.8, Python 3.11
- **Frontend**: Semantic HTML5, Vanilla CSS3, Vanilla JavaScript (ES6+)
- **Database**: SQLite (development)
- **State Management**: LocalStorage for cart and wishlist
- **Image Handling**: Pillow for product images

## Database Models

### Category
- Name, slug, description
- Auto-generated slug from name

### Product
- Name, slug, category, description
- Price and optional original price (for discounts)
- Image, stock quantity
- Featured flag, availability flag
- Automatic discount percentage calculation

### Order
- Customer information (name, email, phone, address)
- Order number (auto-generated)
- Status tracking (pending, processing, shipped, delivered, cancelled)
- Total amount

### OrderItem
- Links products to orders
- Quantity and price at time of purchase
- Subtotal calculation

### ContactMessage
- Customer inquiries with read status

## Architecture

### Frontend Dynamic Functionality
- **cart.js**: Cart management with localStorage, add/remove items, quantity updates
- **wishlist.js**: Wishlist management with localStorage, toggle items
- **main.js**: Mobile menu toggle, notification animations

### URL Structure
- `/` - Home page
- `/shop/` - Product listing with filters
- `/product/<slug>/` - Product detail
- `/cart/` - Shopping cart
- `/wishlist/` - Wishlist
- `/checkout/` - Checkout page
- `/my-account/` - Account dashboard
- `/contact/` - Contact form
- `/why-choose-us/` - Brand information
- `/admin/` - Django admin panel

## Sample Data
The project includes 10 sample products across 4 categories:
- Necklaces (4 products)
- Earrings (3 products)
- Bracelets (2 products)
- Rings (2 products)

Products feature realistic pricing ($49.99 - $1,299.99) with some items showing discounts.

## Development Workflow
The Django development server runs on port 5000:
```bash
python manage.py runserver 0.0.0.0:5000
```

## Admin Access
Create a superuser to access the admin panel at `/admin/`:
```bash
python manage.py createsuperuser
```

## Recent Changes
- **November 24, 2024**: Initial project setup and complete implementation
  - Created Django project structure with shop and pages apps
  - Implemented all models, views, and URL routing
  - Built all page templates with semantic HTML
  - Created elegant CSS styling with jewelry-appropriate color palette
  - Implemented dynamic cart and wishlist with vanilla JavaScript
  - Added sample product data
  - Configured development workflow

## User Preferences
- Use semantic HTML5 for all templates
- Vanilla CSS and JavaScript (no frameworks)
- Elegant, sophisticated design appropriate for jewelry e-commerce
- Dynamic functionality using localStorage for cart and wishlist persistence
- Gold (#d4af37) and black (#1a1a1a) primary color scheme

## Future Enhancements
- Payment gateway integration (Stripe/PayPal)
- User authentication system for secure accounts
- Email notifications for order confirmations
- Admin dashboard improvements
- Product review and rating system
- Advanced search functionality
- Product image galleries
