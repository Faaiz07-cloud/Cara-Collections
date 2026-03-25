from .models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        cart = getattr(request.user, 'cart', None)
        if cart:
            count = cart.items.count()
        else:
            count = 0
    else:
        count = 0
    context = {
        'cart_item_count': count
    }   
    return(context)