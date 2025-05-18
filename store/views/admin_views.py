from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.contrib.auth import authenticate, login
from django.contrib import messages

from store.models.orders import Order
from store.models.product import Products
from store.models.customer import Customer
from store.models.viewlog import ProductView
from store.models.search_history import SearchHistory

@staff_member_required
def admin_dashboard(request):
    total_orders = Order.objects.count()
    total_customers = Customer.objects.count()
    total_products = Products.objects.count()
    total_revenue = Order.objects.aggregate(revenue=Sum('price'))['revenue'] or 0

    top_products = Products.objects.all()[:5]
    top_viewed = (
        ProductView.objects.values('product__name')
        .annotate(view_count=Count('id'))
        .order_by('-view_count')[:5]
    )
    top_searches = (
        SearchHistory.objects.values('query')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    try:
        order_data = (
            Order.objects
            .annotate(order_day=TruncDate('date'))
            .values('order_day')
            .annotate(count=Count('id'), revenue=Sum('price'))
            .order_by('order_day')
        )
    except Exception as e:
        print("🔥 order_data error:", e)
        order_data = []

    category_data = Products.objects.values('category__name').annotate(count=Count('id'))

    context = {
        'total_orders': total_orders,
        'total_customers': total_customers,
        'total_products': total_products,
        'total_revenue': total_revenue,
        'top_products': top_products,
        'top_viewed': top_viewed,
        'top_searches': top_searches,
        'order_data': list(order_data),
        'category_data': list(category_data),
    }

    return render(request, 'admin_dashboard.html', context)

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials or not a staff user.")

    return render(request, 'admin_login.html')
