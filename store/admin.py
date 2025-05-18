from django.contrib import admin
from .models.product import Products
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
from store.models.search_history import SearchHistory
from django.contrib import admin

admin.site.site_header = "ElectroMart Admin"
admin.site.site_title = "ElectroMart Admin Panel"
admin.site.index_title = "Welcome to ElectroMart"



class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

# Register your models here.
admin.site.register(Products,AdminProduct)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(SearchHistory)



# username = Tanushree, email = tanushree7252@gmail.com, password = 1234
