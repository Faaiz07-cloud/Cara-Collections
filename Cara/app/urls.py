from django.urls import path
from .import views

urlpatterns = [
    path('master/', views.Master, name='master'),
    path('', views.Index, name='index'),
    path('shop/', views.Shop, name='shop'),
    path('about/', views.About, name='about'),
    path('contact/', views.Contact, name='contact'),
    path('blog/', views.Blog, name='blog'),
    path('cart/', views.Cart, name='cart'),
    path('product_d/<int:pk>/', views.ProductDetails, name='product_details'),
    path('prod_by_category/<int:pk>/', views.Product_By_Category, name='Product_By_Category'),
    
    #auth urls
    path('signup/', views.SignUp, name='signup'),
    path('login/', views.UserLogin, name='login'),
    path('logout/', views.UserLogout, name='logout'),
]