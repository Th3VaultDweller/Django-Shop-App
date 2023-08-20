from django import forms
from localflavor.us.forms import USZipCodeField
from .models import Order

class OrderCreateForm(forms.ModelForm):
    """Форма создания заказа"""
    # внутренний класс класса модели. Метамодель в основном используется для изменения поведения полей модели, таких как изменение опций заказа, verbose_name, и многих других параметров.
    class Meta: 
        postal_code = USZipCodeField # почтовый индекс в США
        model = Order
        fields = ['first_name',
                'last_name',
                'email',
                'address',
                'postal_code',
                'city']
    