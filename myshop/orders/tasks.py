from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task # декоратор
def order_created(order_id):
    """Задание по отправке уведомления по email при успешном создании заказа"""
    order = Order.objects.get(id=order_id)
    subject = f'Order №{order.id}' # тема сообщения - номер заказа
    message = f'Dear {order.first_name}, \n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
    return mail_sent
