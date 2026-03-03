from django.db import models
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return f"{self.category.name} - {self.name}"
  
class Inventory(models.Model):
    p_name = models.CharField(max_length=200)
    p_img = models.ImageField(upload_to='inventory/')
    p_brand = models.CharField(max_length=100)
    p_price = models.DecimalField(max_digits=10, decimal_places=2) 
    p_rating = models.PositiveSmallIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category', null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='sub_category', null=True, blank=True)

    def __str__(self):
        return self.p_name

class banner(models.Model):
    banner_no = models.CharField(max_length=50)
    banner_img = models.ImageField(upload_to='banners/')   
    banner_title = models.CharField(max_length=200)
    banner_desc = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.banner_no