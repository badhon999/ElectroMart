from django.shortcuts import render, redirect
from store.models.product import Products
from ml.recommendation_engine import generate_recommendations_for_user  # Add this at the top
from store.models.customer import Customer  # if not already imported

def shop_view(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Products.get_all_products()

    size = request.GET.getlist('size')
    color = request.GET.getlist('color')

    if size:
        products = products.filter(size__in=size)
    if color:
        products = products.filter(color__in=color)
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    # Recommendations
    recommended_products = []
    if request.session.get('customer'):
        customer_id = request.session.get('customer')
        recommended_products = generate_recommendations_for_user(customer_id)

    if not recommended_products:
        recommended_products = Products.objects.all().order_by('?')[:4]

    return render(request, 'shop.html', {
        'products': products,
        'recommended_products': recommended_products
    })
