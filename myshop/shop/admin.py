from django.contrib import admin
from .models import Category, Product
from parler.admin import TranslatableAdmin

# Register your models here.

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']
    
    def get_prepopulated_fields(self, request, obj=None): 
        return {'slug':('name',)} # атрибут prepopulated_fields используется для того, чтобы указывать поля автоматически с использованием значения других полей

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'price', 
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available'] # атрибут list_editable используется для того, чтобы задать поля, которые модно редактировать, находясь на странице отображения списка на сайте администрирования
    
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug':('name',)}