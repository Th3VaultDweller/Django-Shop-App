from django.db import models
from django.urls import reverse

class Category(models.Model):
    """Репрезентация категории товара в интернет-магазине"""
    name = models.CharField(max_length=255) # название товара
    slug = models.SlugField(max_length=255, unique=True) # слаг товара для красивого URL-адреса

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name']),]
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])

class Product(models.Model):
    """Репрезентация товара в интернет-магазине"""
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) # для хранения значений денежных сумм всегда следует использовать DecimalField. Используя Decimal удастся избежать проблем с плавающей запятой
    available = models.BooleanField(blank=True) # Булево значение (да или нет)
    created = models.DateTimeField(auto_now_add=True) # auto_now_add добавляет дату и время только на момент создания товара
    updated = models.DateTimeField(auto_now=True) # auto_now добавляет дату и время каждый раз, когда товар обновляется

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])
