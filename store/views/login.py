from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from store.models.customer import Customer

# ✅ Customer login view
def customer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        if customer and customer.check_password(password):
            request.session['customer'] = customer.id
            return redirect('user_dashboard')
        messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html')

# ✅ Admin login view
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            auth_login(request, user)
            return redirect('admin_dashboard')
        messages.error(request, 'Invalid credentials or not admin.')
    return render(request, 'admin_login.html')

# ✅ Logout (clears session)
def logout(request):
    request.session.flush()
    return redirect('login')
