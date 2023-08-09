import os
from celery import Celery

# задать страндартный модуль настроек Django для программы 'celery'

# задается переменная DJANGO_SETTINGS_MODULE для встроенной в Celery программы командной строки
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

# создание экземпляра приложения
app = Celery('myshop')

# используя метод config_from_object(), загружается любая конкретноприкладная конфигурация из настроек проекта. Атрибут namespace задает префикс, который будет в файле settings.py у настроек, связанных с Celery. Задав именное пространство CELERY, все настройки Celery должны включать в свое имя префикс CELERY_ (например, CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')

# сообщается, чтобы очередь заданий Celery автоматически обнаруживала асинхронные задания в приложениях. Celery будет искать файл tasks.py в каждом каталоге приложений, добавленных в INSTALLED_APPS, чтобы загружать определенные в нем асинхронные задания.
app.autodiscover_tasks()