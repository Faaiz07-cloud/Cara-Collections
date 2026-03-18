from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    p_desc = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category', null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='sub_category', null=True, blank=True)

    def __str__(self):
        return self.p_name
    
class ProductGallery(models.Model):
    prod_gallery = models.ImageField(upload_to='prod_gallery/', null=True, blank=True)    
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='prod_gallery')
    
    def __str__(self):
        return f"{self.inventory.p_name} - {self.prod_gallery}"

class banner(models.Model):
    banner_no = models.CharField(max_length=50)
    banner_img = models.ImageField(upload_to='banners/')   
    banner_title = models.CharField(max_length=200)
    banner_desc = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.banner_no
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # extra fields
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profiles/', default='profiles/default.png')
    gender_choices = (
        ('M','Male'),
        ('F','Female'),
        ('O','Other')
    )
    gender = models.CharField(max_length=1, choices=gender_choices, blank=True)
    
    def __str__(self):
        return self.user.username
    
# Automatically create & save profile
@receiver(post_save, sender=User)  
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.subject}"