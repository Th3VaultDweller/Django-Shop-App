from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

# Create your views here.

@require_POST
def cart_add(request, product_id):
    """Добавление в корзину или обновление кол-ва существующих товаров"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
        return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    """Удаление товара из корзины"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    """Представление корзины и её товаров"""
    cart = Cart(request)
    # По каждому товару в корзине создается экземпляр CartAddProductForm, чтобы разрешить изменение количества товара. Форма инициализируется текущим количеством товара, и поле override получает значение True, чтобы при передаче формы на обработку в представление cart_add текущее количество заменялось новым
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    return render(request, 'cart/detail.html', {'cart': cart})