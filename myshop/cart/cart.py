from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self, request):
        """Инициализация корзины"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохранить пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Добавить товар в корзину, либо обновить его количество"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                        'price': str(product.price)
                                        }
        if override_quantity: 
            # булево значение, указывающее, нужно ли заменить количество переданным количеством (True) либо прибавить новое количество к существующему количеству (False).
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
    
    def remove(self, product):
        """Удалить товар из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]            
            self.save()
    
    def __iter__(self):
        # функция __iter__ создаёт итератор из последовательности
        # метод __iter__() позволит легко прокручивать товарные позиции корзины в представлениях и шаблонах.
        """Прокрутка товарных позиций и получение товаров из базы данных """
        product_ids = self.cart.keys() 
        # получить объекты product и добавить их в корзину
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        # текущая корзина копируется в  переменную cart, и в нее добавляются экземпляры класса Product.
        for product in products:
            cart[str(product.id)]['product'] = product
        
        # товары корзины прокручиваются в цикле, конвертируя цену каждого товара обратно в десятичное число фиксированной точности и добавляя в каждый товар атрибут total_price
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
        

    def __len__(self):
        """Подсчёт всех товарных попозиций в корзине"""
        return sum(item['quantity']
                   for item in self.cart.values())
    
    def get_total_price(self):
        """Подсёт общей стоимости товаров в корзине"""
        return sum(Decimal(item['price']) *item['quantity']
                   for item in self.cart.values())

    def save(self):
        """Пометить сеанс как изменённый, чтобы обеспечить его сохранение"""
        self.session.modified = True
    
    def clear(self):
        """Удаление корзины из сеанса"""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    