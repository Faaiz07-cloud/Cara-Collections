from django.contrib import admin

# Register your models here.
from .models import Category, SubCategory, Inventory, ProductGallery, banner, UserProfile

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1
    can_delete = True
    fk_name = 'category'

class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]
    list_display = ('name', 'image', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')
admin.site.register(Category, CategoryAdmin)

class ProdGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1
    can_delete = True
    fk_name = 'inventory'

class InventoryAdmin(admin.ModelAdmin):
    inlines = [ProdGalleryInline]
    list_display = ('p_name', 'p_img', 'p_brand', 'p_price', 'p_rating', 'is_featured', 'category', 'sub_category', 'p_desc', 'created_at')
    list_filter = ('is_featured', 'created_at', 'category', 'sub_category')
    search_fields = ('p_name', 'category__name', 'sub_category__name')
    readonly_fields = ('created_at', 'updated_at')
admin.site.register(Inventory, InventoryAdmin)

class BannerAdmin(admin.ModelAdmin):
    list_display = ('banner_no', 'banner_img', 'banner_title', 'banner_desc', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('banner_no', 'banner_title')
    readonly_fields = ('created_at',)
admin.site.register(banner, BannerAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = (  
        'get_username', 
        'get_first_name', 
        'get_last_name', 
        'get_email', 
        'phone', 
        'address', 
        'profile_pic', 
        'gender'
    )

    list_filter = ('gender',)

    search_fields = ('user__username',)

    # Methods to get related User fields
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

admin.site.register(UserProfile, ProfileAdmin)