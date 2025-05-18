from django.urls import path
from .views.signup import Signup
from .views.login import customer_login, admin_login, logout
from .views.cart import Cart
from .views.checkout import CheckOut
from .views.orders import OrderView
from .views.shop import shop_view
from .views.ar_vr import ar_vr_view
from .views.home import (
    Index, ProductDetail, search_view, store,
    admin_dashboard, user_dashboard, edit_profile
)
from .middlewares.auth import auth_middleware

urlpatterns = [
    # Main Pages
    path('', Index.as_view(), name='homepage'),
    path('store/', store, name='store'),
    path('shop/', shop_view, name='shop'),
    path('product/<int:product_id>/', ProductDetail.as_view(), name='product_detail'),
    # Authentication
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', customer_login, name='login'),  # Customer login
    path('login/admin/', admin_login, name='admin_login'),  # Admin login
    path('logout/', logout, name='logout'),

    # Customer & Admin Dashboards
    path('my-dashboard/', user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('edit-profile/', edit_profile, name='edit_profile'),

    # Orders & Checkout
    path('cart/', auth_middleware(Cart.as_view()), name='cart'),
    path('check-out/', CheckOut.as_view(), name='checkout'),
    path('orders/', auth_middleware(OrderView.as_view()), name='orders'),

    # Search
    path('search/', search_view, name='search'),
]
