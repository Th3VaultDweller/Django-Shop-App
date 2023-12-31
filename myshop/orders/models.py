from django.db import models
from shop.models import Product
from django.utils.translation import gettext_lazy as _ # перевод

# Create your models here.

class Order(models.Model):
    """Репрезентация заказа с информацией о клиенте"""
    first_name = models.CharField(_('first_name'),
                                  max_length=100)
    last_name = models.CharField(_('last_name'),
                                 max_length=100)
    email = models.EmailField(_('email'))
    address = models.CharField(_('address'),
                               max_length=250)
    postal_code = models.CharField(_('postal_code'),
                                   max_length=20)
    city = models.CharField(_('city'),
                            max_length=250)
    created = models.DateField(auto_now_add=True) # auto_now_add добавляет дату и время только на момент создания товара
    updated = models.DateField(auto_now=True) # auto_now добавляет дату и время каждый раз, когда товар обновляется
    paid = models.BooleanField(default=False) # булево значение: оплачен заказ или нет

    class Meta:
        ordering = ['-created'] # вывод списка в обратном порядке
        indexes = [models.Index(fields=['-created']),]
    
    def __str__(self):
        return f'Order {self.id}' # f-строка
    
    def get_total_cost(self):
        """Получение общей стоимости товаров в заказе"""
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    """Сохранение товара, количества и цены, уплаченной за каждый товар"""
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE) # CASCADE автоматически удаляет строку из зависимой таблицы, если удаляется связанная строка из главной таблицы
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        "Стоимость товара"
        return self.price * self.quantity # цена за товар, помноженная на его количество