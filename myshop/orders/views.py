from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

# Create your views here.

def order_create(request):
    """Создание заказа"""
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            # товарные позиции прокручиваются в цикле, для каждой позиции создаётся OrderItem
            for item in cart:
                OrderItem.objects.create(order=order,
                                         products=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                
                cart.clear() # очистка корзины
                return render(request,'orders/order/created.html',
                              {'order': order})
        else:
            form = OrderCreateForm()
        
        return render(request,'orders/order/create.html',
                      {'cart': cart, 'form': form})

