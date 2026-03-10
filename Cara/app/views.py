from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from .forms import SignUpForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from app.models import Category, SubCategory, Inventory,  banner

def Master(request):
    return render(request,'master.html')

@login_required
def Index(request):
    categories = Category.objects.all()
    featured_inventory = Inventory.objects.filter(is_featured=True).order_by('-id')

    fifteen_days_ago = timezone.now() - timedelta(days=15)
    new_arrivals_inventory = Inventory.objects.filter(created_at__gte=fifteen_days_ago).order_by('-id')
    context = {
        'categories': categories,
        'featured_inventory': featured_inventory,
        'new_arrivals_inventory': new_arrivals_inventory
    }
    return render(request,'index.html', context)    

def Shop(request):
    all_products = Inventory.objects.all().order_by('-id')
    context = {
        'all_products': all_products
    }
    return render(request,'shop.html', context)   

def About(request):
    return render(request,'about.html')

def Contact(request):
    return render(request,'contact.html')

def Blog(request):
    banners = banner.objects.filter(is_active=True)
    context = {
        'banners' : banners
    }
    return render(request,'blog.html', context)

def Cart(request):
    return render(request,'cart.html')

def ProductDetails(request, pk):
    product = get_object_or_404(Inventory, pk=pk)
    featured_inventory = Inventory.objects.filter(is_featured=True).order_by('-id')
    context = {
        'product': product,
        'featured_inventory': featured_inventory
    }
    
    return render(request,'product_details.html', context)

def Product_By_Category(request, pk):
    
    #First get id of clicked sub_category
    sub_category = get_object_or_404(SubCategory, pk=pk)
    
    #Now fetch products that matches the sub_category id
    products = Inventory.objects.filter(sub_category=sub_category).order_by('-id')
    
    featured_inventory = Inventory.objects.filter(is_featured=True).order_by('-id')
    context = {
       'category' : sub_category.category,
       'sub_category': sub_category,
       'products': products,
       'featured_inventory': featured_inventory
    }

    return render(request, 'prod_by_category.html', context)

def SignUp(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "User successfully SignUp!")
            return redirect('index')
        
    context = {
        'form': form
    }    
    return render(request, 'signup.html', context)

def UserLogin(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "User successfully Login!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password!")
    context = {
        'form': form
    }
    return render(request, 'login.html', context)    

def UserLogout(request):
    logout(request)
    messages.success(request, "User successfully Logout!")
    return redirect('login')


