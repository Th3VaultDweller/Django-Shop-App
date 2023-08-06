from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'fist_name',
                    'last_name',
                    'email',
                    'address',
                    'postal code',
                    'city',
                    'paid',
                    'created',
                    'updated']
    
    list_filter = ['created',
                   'updated',
                   'paid']
    inlines = [OrderItemInLine]