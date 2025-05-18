from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from django.contrib import messages
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.contrib.admin.views.decorators import staff_member_required

from store.models.product import Products
from store.models.category import Category
from store.models.customer import Customer
from store.models.orders import Order
from store.models.search_history import SearchHistory
from store.models.viewlog import ProductView
from ml.recommendation_engine import generate_recommendations_for_user

# -------------------------------
# Homepage Product Display
# -------------------------------

def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}

    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')

    if categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)
    else:
        products = Products.get_all_products()

    recommended_products = []
    if request.session.get('customer'):
        customer_id = request.session.get('customer')
        recommended_products = generate_recommendations_for_user(customer_id)

    if not recommended_products:
        recommended_products = Products.objects.all().order_by('?')[:4]

    return render(request, 'index.html', {
        'products': products,
        'categories': categories,
        'recommended_products': recommended_products,
    })

# -------------------------------
# Product Detail with View Logging
# -------------------------------

class ProductDetail(View):
    def get(self, request, product_id):
        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return render(request, "404.html")

        customer = None
        customer_id = request.session.get('customer')
        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                pass

        ProductView.objects.create(product=product, customer=customer)
        return render(request, "product_detail.html", {"product": product})

# -------------------------------
# Search Functionality
# -------------------------------

def search_view(request):
    query = request.GET.get('q')
    results = []

    if query and request.session.get('customer'):
        try:
            customer_id = request.session.get('customer')
            customer = Customer.objects.get(id=customer_id)
            SearchHistory.objects.create(customer=customer, query=query)
        except Customer.DoesNotExist:
            pass

    if query:
        results = Products.objects.filter(name__icontains=query)

    return render(request, 'search_results.html', {'results': results})

# -------------------------------
# Index View (Cart Handling)
# -------------------------------

class Index(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart', {})

        if product in cart:
            if remove:
                if cart[product] <= 1:
                    cart.pop(product)
                else:
                    cart[product] -= 1
            else:
                cart[product] += 1
        else:
            cart[product] = 1

        request.session['cart'] = cart
        return redirect('homepage')

    def get(self, request):
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

# -------------------------------
# User Dashboard
# -------------------------------

def user_dashboard(request):
    customer_id = request.session.get('customer')
    if not customer_id:
        return render(request, 'login.html', {'error': 'Please log in to access your dashboard.'})

    customer = Customer.objects.get(id=customer_id)
    orders = Order.get_orders_by_customer(customer_id)
    recommendations = generate_recommendations_for_user(customer_id)

    return render(request, 'user_dashboard.html', {
        'customer': customer,
        'orders': orders,
        'recommended_products': recommendations
    })

# -------------------------------
# Edit Profile
# -------------------------------

def edit_profile(request):
    customer_id = request.session.get('customer')
    if not customer_id:
        return redirect('login')

    customer = Customer.objects.get(id=customer_id)

    if request.method == 'POST':
        customer.first_name = request.POST.get('first_name')
        customer.last_name = request.POST.get('last_name')
        customer.phone = request.POST.get('phone')
        customer.email = request.POST.get('email')
        customer.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('user_dashboard')

    return render(request, 'edit_profile.html', {'customer': customer})

# -------------------------------
# Admin Dashboard (for staff)
# -------------------------------

@staff_member_required
def admin_dashboard(request):
    total_orders = Order.objects.count()
    total_customers = Customer.objects.count()
    total_products = Products.objects.count()
    total_revenue = sum(order.price * order.quantity for order in Order.objects.all())

    top_products = Products.objects.all()[:5]
    top_viewed = ProductView.objects.values('product__name').annotate(view_count=Count('id')).order_by('-view_count')[:5]
    top_searches = SearchHistory.objects.values('query').annotate(count=Count('id')).order_by('-count')[:5]

    order_data = (
        Order.objects
        .annotate(date=TruncDate('date'))
        .values('date')
        .annotate(count=Count('id'), revenue=Sum('price'))
        .order_by('date')
    )

    category_data = Products.objects.values('category__name').annotate(count=Count('id'))

    return render(request, 'admin_dashboard.html', {
        'total_orders': total_orders,
        'total_customers': total_customers,
        'total_products': total_products,
        'total_revenue': total_revenue,
        'top_products': top_products,
        'top_viewed': top_viewed,
        'top_searches': top_searches,
        'order_data': list(order_data),
        'category_data': list(category_data),
    })
