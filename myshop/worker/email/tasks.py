from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import get_object_or_404

from order.models import Order
from worker.app import app


@app.task(
    max_retries=5, default_retry_delay=60, auto_retry_for=(ConnectionRefusedError,)
)
def send_order_placement_mail(host, order_pk):
    """Sending order placement mail to user who finished placing an order
    successfully.

    """

    order = get_object_or_404(Order, pk=order_pk)
    mail_sent = send_mail(
        f"Thank you, {order.first_name}! Order #{order.pk} has been confirmed.",
        f"Dear, {order.first_name}. Your order has been placed successfully.\n"
        f"Your order number is #{order.pk}.\n"
        f"Now you are able to proceed with the payment:\n"
        f"http://{host}" + reverse("order:order_detail", kwargs={"pk": order_pk}),
        "admin@myshop.com",
        [order.email],
    )

    return mail_sent


@app.task
def debug_task(self):
    print(f"Request: {self.request!r}")  # pragma: no cover
