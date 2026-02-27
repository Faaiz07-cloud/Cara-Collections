from django.contrib import admin

# Register your models here.
from .models import Category, SubCategory

admin.site.register(Category)
admin.site.register(SubCategory)
