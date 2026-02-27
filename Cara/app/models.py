from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    rating = models.PositiveSmallIntegerField(default=0) 

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images') 

    def __str__(self):
        return f"Image for {self.product.name}"           