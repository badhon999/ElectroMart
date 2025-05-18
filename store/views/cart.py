from django.shortcuts import render, redirect
from django.views import View
from store.models.product import Products

class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart', {}).keys())
        products = Products.get_products_by_id(ids)
        return render(request, 'cart.html', {'products': products})

    def post(self, request):
        product_id = request.POST.get('product_id')
        remove = request.POST.get('remove')
        cart = request.session.get('cart', {})

        if product_id:
            quantity = cart.get(product_id, 0)

            if remove:
                if quantity <= 1:
                    cart.pop(product_id, None)
                else:
                    cart[product_id] = quantity - 1
            else:
                cart[product_id] = quantity + 1

            request.session['cart'] = cart

        return redirect('/cart')

