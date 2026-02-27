from django.shortcuts import render

from app.models import Category, SubCategory, Product, ProductImage, NewArrivalProduct, NewArrivalProductImage

def Master(request):
    return render(request,'master.html')

def Index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    new_arrival_products = NewArrivalProduct.objects.all()
    context = {
        'categories': categories,
        'products': products,
        'new_arrival_products': new_arrival_products
    }
    return render(request,'index.html', context)    

def Shop(request):
    return render(request,'shop.html')   

def About(request):
    return render(request,'about.html')

def Contact(request):
    return render(request,'contact.html')

def Blog(request):
    return render(request,'blog.html')

def Cart(request):
    return render(request,'cart.html')

def ProductDetails(request):
    return render(request,'product_details.html')