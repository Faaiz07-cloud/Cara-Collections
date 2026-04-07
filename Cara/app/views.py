from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from app.models import Category, SubCategory, Inventory,  banner, Cart, CartItem, OrderItem, Order, ProductGallery
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from .forms import SignUpForm
from .forms import LoginForm
from .forms import ProfileForm
from .forms import ContactForm
from .forms import InventoryForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Contact
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

# Admin Views
def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def master_admin(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('login')
    
    return render(request, 'admin_dashboard/master_admin.html')

@user_passes_test(is_superuser)
def admin_dashboard(request):
    products = Inventory.objects.all().order_by('-created_at')
    context = {
     'products': products
    }

    return render(request, 'admin_dashboard/dashboard.html', context)

@user_passes_test(is_superuser)
def add_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST, request.FILES)
        multiple_files = request.FILES.getlist('prod_gallery')
        if form.is_valid():
            product = form.save()
            for file in multiple_files:
                ProductGallery.objects.create(prod_gallery=file, inventory=product)
            messages.success(request, "Product added successfully.")
            return redirect('admin_dashboard')
    else:
        form = InventoryForm()
        context = {
         'form': form
        }

        return render(request, 'admin_dashboard/add_inventory.html', context)

@user_passes_test(is_superuser)
def AdminProductDetails(request, pk):
    product = get_object_or_404(Inventory, pk=pk)
    context = {
    'product': product,
    }

    return render(request,'admin_dashboard/admin_product_details.html', context)   

@user_passes_test(is_superuser)
def delete_product(request, pk):
    product = get_object_or_404(Inventory, pk=pk)
    
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('admin_dashboard')

# Public Views
def Master(request):
    return render(request,'master.html')

def Index(request):
    categories = Category.objects.all()
    featured_inventory = Inventory.objects.filter(is_featured=True).order_by('-id')

    fifteen_days_ago = timezone.now() - timedelta(days=15)
    new_arrivals_inventory = Inventory.objects.filter(created_at__gte=fifteen_days_ago).order_by('-id')
     
    context = {
    'categories': categories,
    'featured_inventory': featured_inventory,
    'new_arrivals_inventory': new_arrivals_inventory,
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

@login_required
def ContactView(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            user = User.objects.get(username=username, email=email)

            # save in db - contact model
            Contact.objects.create(
            user =user,
            subject =subject,
            message =message,
            )

            # send email to user
            subject_user = "Thanks for contacting us"
            from_email = settings.EMAIL_HOST_USER
            to_email = [email]

            html_content_user = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height:1.5; color: #333;">
            <h2 style="color: #2E86C1;">Hi {username},</h2>
            <p>Thank you for contacting us. We have received your request and our support team will get back to you shortly.</p>
            <hr>
            <h4>Your Submitted Details:</h4>
            <ul>
            <li><strong>Username:</strong> {username}</li>
            <li><strong>Email:</strong> {email}</li>
            <li><strong>Subject:</strong> {subject}</li>
            <li><strong>Message:</strong> {message}</li>
            </ul>
            <p>We appreciate your patience!</p>
            <br>
            <p>— The Cara Collections Team</p>
            </body>
            </html>
            """

            msg_user = EmailMultiAlternatives(subject_user, "", from_email, to_email)
            msg_user.attach_alternative(html_content_user, "text/html")
            msg_user.send()

            # send email to admin
            subject_admin = f"[Support Request] {username} - {subject}"
            from_email = settings.EMAIL_HOST_USER
            to_email = [settings.EMAIL_HOST_USER,]

            html_content_admin = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height:1.5; color: #333;">
            <h2 style="color: #C0392B;">New Contact Request</h2>
            <p>A user has submitted a contact request:</p>
            <ul>
            <li><strong>Username:</strong> {username}</li>
            <li><strong>Email:</strong> {email}</li>
            <li><strong>Subject:</strong> {subject}</li>
            <li><strong>Message:</strong> {message}</li>
            </ul>
            <p>Please follow up and resolve the request as soon as possible.</p>
            <br>
            <p>— Cara Collections System</p>
            </body>
            </html>
            """

            msg_admin = EmailMultiAlternatives(subject_admin, "", from_email, to_email)
            msg_admin.attach_alternative(html_content_admin, "text/html")
            msg_admin.send()

            return redirect('contact_success')
        context = {
        'form': form
        }
        return render(request,'contact.html', context)
    else:
        form = ContactForm()
        context = {
        'form': form
        }
        return render(request,'contact.html', context)

def ContactSuccess(request):
    return render(request, "contact_success.html")

def Blog(request):
    banners = banner.objects.filter(is_active=True).order_by('-id')
    context = {
    'banners' : banners
    }
    return render(request,'blog.html', context)

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
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        context = {
        'form': form    
        }
        return render(request, 'signup.html', context)
    else:
        form = SignUpForm()
        context = {
        'form': form
        }
        return render(request, 'signup.html', context)

def Login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
              login(request, user)
              if user.is_superuser:
                  return redirect('admin_dashboard')
              else:
                  return redirect('index')
        context = {
        'form': form    
        }
        return render(request, 'login.html', context)
    else:
        form = LoginForm()
        context = {
        'form': form
        }
        return render(request, 'login.html', context)

def Logout(request):
    logout(request)
    return redirect('index')

@login_required
def edit_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
        context = {
        'form': form
        }
        return render(request, 'edit_profile.html', context)

@login_required
def profile(request):
    profile = request.user.userprofile
    context = {
    'profile': profile
    }
    return render(request, 'profile.html', context)

# Cart Views
@login_required
def cart_add(request, id):
    # Get the user's cart (already auto-created by signal)
    cart = request.user.cart

    # Get the Product
    product = get_object_or_404(Inventory, id=id)

    # Check if product already in cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
 
    if not created:
        #Already exists, just increment quantity
        cart_item.quantity += 1
        cart_item.save()

    # Show success message
    messages.success(request, 'Added to cart!') 

    # Redirect to next url or home
    next_url = request.GET.get('next', '/')
    return redirect(next_url)

@login_required
def cart_detail(request):
    # Get the user's cart (already auto-created by signal)
    cart = request.user.cart

    # Get all cart items
    cart_items = cart.items.all()

    # Calculate Total
    total = sum(item.get_total_price() for item in cart_items)

    if total >= 500:
        shipping_fee = 0
    else:
        shipping_fee = 30

    new_total = total + shipping_fee 

    context = {
        'cart_items': cart_items,
        'shipping_fee': shipping_fee,
        'total': total,
        'new_total': new_total,
    }      

    return render(request, 'cart.html', context)

def item_clear(request, id):
    cart_item = get_object_or_404(CartItem, id=id, cart=request.user.cart)
    cart_item.delete()
    return redirect('cart_detail')

def item_increment(request, id):
   cart_item = get_object_or_404(CartItem, id=id, cart=request.user.cart)
   cart_item.quantity += 1
   cart_item.save()
   return redirect('cart_detail')

def item_decrement(request, id):
    cart_item = get_object_or_404(CartItem, id=id, cart=request.user.cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart_detail')

def cart_clear(request):
    cart = request.user.cart
    cart.items.all().delete()
    return redirect('cart_detail')

@login_required
def CheckoutView(request):
    cart = request.user.cart
    cart_items = cart.items.all()

    total = sum(item.get_total_price() for item in cart_items)
    shipping_fee = 0 if total >= 500 else 30
    new_total = total + shipping_fee

    context = {
        'cart_items': cart_items,
        'total': total,
        'shipping_fee': shipping_fee,
        'new_total': new_total,
    }
    return render(request, 'checkout.html', context)

@login_required
def PlaceOrder(request):
    if request.method == 'POST':
        cart = request.user.cart
        cart_items = cart.items.all()

        if not cart_items:
            messages.warning(request, "Your cart is empty!")
            return redirect('checkout')

        # Get form data
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        notes = request.POST.get('notes')
        payment_method = request.POST.get('payment_method')

        # Calculate totals
        total_price = sum(item.get_total_price() for item in cart_items)
        shipping_fee = 0 if total_price >= 500 else 30
        new_total = total_price + shipping_fee

        # Create Order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            notes=notes,
            payment_method=payment_method,
            total_price=new_total
        )

        # Create OrderItems
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.get_total_price()
            )

        # Build HTML items table
        items_html = ""
        for item in cart_items:
            items_html += f"""
            <tr>
               <td style="padding: 8px; border: 1px solid #ddd;">{item.product.p_name}</td>
               <td style="padding: 8px; border: 1px solid #ddd; text-align:center;">{item.quantity}</td>
               <td style="padding: 8px; border: 1px solid #ddd; text-align:right;">Rs. {item.get_total_price()}</td>
            </tr>
            """

        # Shipping display
        shipping_display = "Free" if shipping_fee == 0 else f"Rs. {shipping_fee}.0"

        # Complete HTML message
        html_message = f"""
        <html>
        <head>
            <style>
               body {{ font-family: Arial, sans-serif; color: #333; }}
               .container {{ width: 600px; margin: 0 auto; }}
               h2 {{ color: #2E86C1; }}
               table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
               th, td {{ border: 1px solid #ddd; padding: 8px; }}
               th {{ background-color: #f2f2f2; text-align: left; }}
            </style>
        </head>
        <body>
            <div class="container">
              <h2>Hi {order.full_name},</h2>
              <p>Your order has been placed successfully!</p>
              <h3>Order Details:</h3>
              <p><strong>Order ID:</strong> {order.id}</p>

              <table>
                <thead>
                    <tr>
                      <th>Product</th>
                      <th>Quantity</th>
                      <th>Price</th>
                    </tr>
                </thead>
                <tbody>
                    {items_html}
                </tbody>
              </table>

              <p><strong>Subtotal:</strong> Rs. {total_price}<br>
              <strong>Shipping:</strong> {shipping_display}<br>
              <strong>Total Amount:</strong> Rs. {order.total_price}<br>
              <strong>Payment Method:</strong> {order.payment_method}</p>

              <p><strong>Shipping Address:</strong><br>
                {order.address}</p>

              <p>Thank you for shopping with us ❤️</p>
              <br>
              <br>
              <p>Cara Collections Team</p>
            </div>
        </body>
        </html>
        """ 
        
        email = EmailMessage(
         subject=f"Order Confirmation - Order #{order.id}",
         body=html_message,
         from_email=settings.EMAIL_HOST_USER,
         to=[order.email],
        )
        email.content_subtype = "html"  # Important: tells Django this is HTML
        email.send(fail_silently=False)

        # Clear cart
        cart.items.all().delete()

        return redirect('order_success', order_id=order.id)

@login_required
def OrderSuccess(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order,
        'total': order.total_price,
    }
    return render(request, 'order_success.html', context)