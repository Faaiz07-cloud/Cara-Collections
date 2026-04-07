from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm
from .forms import CustomSetPasswordForm

urlpatterns = [
    path('master/', views.Master, name='master'),
    path('', views.Index, name='index'),
    path('shop/', views.Shop, name='shop'),
    path('about/', views.About, name='about'),
    path('blog/', views.Blog, name='blog'),
    path('product_d/<int:pk>/', views.ProductDetails, name='product_details'),
    path('prod_by_category/<int:pk>/', views.Product_By_Category, name='Product_By_Category'),

    # auth urls
    path('signup/', views.SignUp, name='signup'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # forgot password urls

    # Page where user enters email to request password reset
    path('forgot-password/', auth_views.PasswordResetView.as_view(template_name='forgot_password.html', form_class=CustomPasswordResetForm), name='password_reset'),

    # Shows message that password reset email has been sent
    path('forgot-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='forgot_password_done.html'), name='password_reset_done'),

    # Link from email where user sets a new password
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=CustomSetPasswordForm), name='password_reset_confirm'),

    # Confirmation page after password has been successfully reset
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    
    # Contact Urls
    path('contact/', views.ContactView, name='contact'),
    path('contact_success/', views.ContactSuccess, name='contact_success'),

    # Cart Urls
    path('cart-detail/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),

    # Checkout Urls
    path('checkout/', views.CheckoutView, name='checkout'),
    path('place-order/', views.PlaceOrder, name='place_order'),
    path('order-success/<int:order_id>/', views.OrderSuccess, name='order_success'),

    # Admin Urls
    path('master_admin/', views.master_admin, name='master_admin'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_product/', views.add_inventory, name='add_inventory'),
    path('admin_product_d/<int:pk>/', views.AdminProductDetails, name='admin_product_details'),
    path('product_delete/<int:pk>/', views.delete_product, name='delete_product'),
]