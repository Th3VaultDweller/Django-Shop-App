from django.db import models
from shop.models import Product

# Create your models here.

class Order(models.Model):
    """Репрезентация заказа с информацией о клиенте"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField() # без лимита - на случай очень длинных названий
    address = models.CharField()
    postal_code = models.CharField(max_length=20)
    city = models.CharField()
    created = models.DateField(auto_now_add=True) # # auto_now_add добавляет дату и время только на момент создания товара
    updated = models.DateField(auto_now=True) # auto_now добавляет дату и время каждый раз, когда товар обновляется
    paid = models.BooleanField(default=False) # булево значение: оплачен заказ или нет

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created']),]
    
    def __str__(self):
        return f'Order {self.id}' # f-строка
    
    def get_total_cost(self):
        """Получение общей стоимости товаров в заказе"""
        return sum(item.get_cost()) for item in self.items.all()
