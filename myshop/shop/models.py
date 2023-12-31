from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields

class Category(TranslatableModel):
    """Репрезентация категории товара в интернет-магазине"""
    # переводные поля модели, сгенерированные Parler'ом
    translations = TranslatedFields(
        name = models.CharField(max_length=255), # название товара
        slug = models.SlugField(max_length=255, unique=True) # слаг товара для красивого URL-адреса
    )

    # внутренний класс класса модели. Метамодель в основном используется для изменения поведения полей модели, таких как изменение опций заказа, verbose_name, и многих других параметров.
    class Meta:
        # ordering = ['name']
        # indexes = [models.Index(fields=['name']),]
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])

class Product(TranslatableModel):
    """Репрезентация товара в интернет-магазине"""
    # переводные поля модели, сгенерированные Parler'ом
    translations = TranslatedFields(
        name = models.CharField(max_length=255),
        slug = models.SlugField(max_length=255),
        description = models.TextField(blank=True),
    )
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE) # CASCADE автоматически удаляет строку из зависимой таблицы, если удаляется связанная строка из главной таблицы
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) # для хранения значений денежных сумм всегда следует использовать DecimalField. Используя Decimal удастся избежать проблем с плавающей запятой
    available = models.BooleanField(blank=True) # Булево значение (да или нет)
    created = models.DateTimeField(auto_now_add=True) # auto_now_add добавляет дату и время только на момент создания товара
    updated = models.DateTimeField(auto_now=True) # auto_now добавляет дату и время каждый раз, когда товар обновляется

    class Meta:
        # ordering = ['name']
        indexes = [
            # models.Index(fields=['id', 'slug']),
            # models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])
