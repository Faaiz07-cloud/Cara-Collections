from django.contrib import admin

# Register your models here.
from .models import Category, SubCategory, Product, ProductImage, NewArrivalProduct, NewArrivalProductImage, banner

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(NewArrivalProduct)
admin.site.register(NewArrivalProductImage)

class BannerAdmin(admin.ModelAdmin):
    list_display = ('banner_no', 'banner_img', 'banner_title', 'banner_desc', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('banner_no', 'banner_title')
    readonly_fields = ('created_at',)
admin.site.register(banner, BannerAdmin)
