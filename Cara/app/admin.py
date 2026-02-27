from django.contrib import admin

# Register your models here.
from .models import Category, SubCategory, Product, ProductImage, NewArrivalProduct, NewArrivalProductImage

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(NewArrivalProduct)
admin.site.register(NewArrivalProductImage)

