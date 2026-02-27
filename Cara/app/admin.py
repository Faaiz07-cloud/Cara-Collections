from django.contrib import admin

# Register your models here.
from .models import Category, SubCategory, Product, ProductImage

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(ProductImage)
