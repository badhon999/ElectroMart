# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from store.models.customer import Customer
from store.models.product import Products
from store.models.search_history import SearchHistory
from store.models.viewlog import ProductView

class ElectroMartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = Customer.objects.create(
            first_name="Test", last_name="User", phone="0123456789",
            email="test@example.com", password="testpass"
        )
        self.product = Products.objects.create(
            name="Test Product", price=1000, description="A test product", image="test.jpg"
        )
        self.client.session['customer'] = self.customer.id
        self.client.session.save()

    def test_signup_page(self):
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_search_creates_history(self):
        self.client.session['customer'] = self.customer.id
        self.client.session.save()
        response = self.client.get('/search?q=test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SearchHistory.objects.count(), 1)

    def test_add_product_to_cart(self):
        response = self.client.post('/cart', {'product_id': str(self.product.id)})
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertIn(str(self.product.id), self.client.session['cart'])

    def test_checkout_redirect(self):
        session = self.client.session
        session['cart'] = {str(self.product.id): 1}
        session['customer'] = self.customer.id
        session.save()
        response = self.client.post('/check-out', {'address': 'Dhaka', 'phone': '0123456789'})
        self.assertIn(response.status_code, [302, 303])

    def test_product_view_log(self):
        ProductView.objects.create(customer=self.customer, product=self.product)
        self.assertEqual(ProductView.objects.count(), 1)
