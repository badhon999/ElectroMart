from django.db import models
from .category import Category
class Products(models.Model):
    size = models.CharField(max_length=20, choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')], default='M')
    color = models.CharField(max_length=20, choices=[('Black', 'Black'), ('White', 'White'), ('Red', 'Red'), ('Blue', 'Blue'), ('Green', 'Green')], default='Black')
    name = models.CharField(max_length=60)
    price= models.IntegerField(default=0)
    category= models.ForeignKey(Category,on_delete=models.CASCADE,default=1 )
    description= models.CharField(max_length=250, default='', blank=True, null= True)
    image= models.ImageField(upload_to='uploads/products/')
    ar_url = models.URLField(max_length=200, blank=True, null=True)
    vr_url = models.URLField(max_length=200, blank=True, null=True)
    has_ar = models.BooleanField(default=False)
    has_vr = models.BooleanField(default=False)

    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter (id__in=ids)
    @staticmethod
    def get_all_products():
        return Products.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Products.objects.filter (category=category_id)
        else:
            return Products.get_all_products();
