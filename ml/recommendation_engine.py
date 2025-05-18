# ml/recommendation_engine.py

import pandas as pd
from store.models.orders import Order
from store.models.search_history import SearchHistory
from store.models.viewlog import ProductView
from store.models.product import Products
from store.models.customer import Customer
from django.db.models import Count

def generate_recommendations_for_user(user_id, top_n=5):
    """
    Simple scoring-based recommendation using search, views, and orders.
    """
    try:
        customer = Customer.objects.get(id=user_id)
    except Customer.DoesNotExist:
        return Products.objects.all().order_by('?')[:top_n]  # fallback for unknown user

    # 1. Get product IDs from orders
    order_products = Order.objects.filter(customer=customer).values_list('product_id', flat=True)

    # 2. Get product IDs from views
    viewed_products = ProductView.objects.filter(customer=customer).values_list('product_id', flat=True)

    # 3. Get product names from search history
    search_queries = SearchHistory.objects.filter(customer=customer).values_list('query', flat=True)

    searched_products = Products.objects.none()
    for query in search_queries:
        matched = Products.objects.filter(name__icontains=query)
        searched_products = searched_products | matched

    # Merge all product IDs with weights
    score = {}
    for pid in order_products:
        score[pid] = score.get(pid, 0) + 5
    for pid in viewed_products:
        score[pid] = score.get(pid, 0) + 2
    for product in searched_products:
        score[product.id] = score.get(product.id, 0) + 3

    sorted_ids = sorted(score, key=score.get, reverse=True)
    recommended = Products.objects.filter(id__in=sorted_ids).order_by('-id')[:top_n]

    return recommended
