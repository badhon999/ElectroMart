from django.shortcuts import render, redirect
import stripe
from django.conf import settings

from store.models.customer import Customer
import logging
from django.views import View

# Set up logger
logger = logging.getLogger(__name__)

from store.models.product import Products
from store.models.orders import Order

stripe.api_key = ''
class CheckOut(View):
    def post(self, request):
        # Set your secret key. Remember to switch to your live secret key in production!
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

        address = request.POST.get('address')
        phone = request.POST.get('phone')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.keys()))

        
        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email='customer@example.com',
                submit_type='donate',
                billing_address_collection='auto',
                shipping_address_collection={
                  'allowed_countries': ['BD'],
                },
                line_items=[
                    {
                        'price': '{{PRICE_ID}}',  
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url='/success.html',
                cancel_url='/cancel.html',
            )
        except Exception as e:
            logger.error(f"Error during checkout session creation: {str(e)}")
            return render(request, 'checkout.html', {'error': 'An error occurred during checkout. Please try again.'})
        return redirect(checkout_session.url, code=303)
    def fulfill_checkout(session_id):
        	print("Fulfilling Checkout Session", session_id)
