from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.views import generic

from cart.cart import Cart
from worker.email.tasks import send_order_placement_mail
from .forms import OrderModelForm
from .models import Order, OrderItem


class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    """
    TODO
    """

    template_name = "order/order_form.html"
    model = Order
    form_class = OrderModelForm

    def form_valid(self, form):
        """
        TODO
        """
        cart = Cart(self.request)
        self.object = form.save(commit=False)
        self.object.save()
        for item in cart:
            OrderItem.objects.create(
                order=self.object,
                product=item["product"],
                quantity=item["quantity"],
                price=item["price"],
            )
        cart.clear()
        host = get_current_site(self.request).domain
        send_order_placement_mail.delay(host, self.object.pk)
        return super().form_valid(form)

    def get_success_url(self):
        """
        TODO
        """
        return reverse("order:order_detail", kwargs={"pk": self.object.pk})


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    """
    TODO
    """

    model = Order
    template_name = "order/order_detail.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        """
        TODO
        """
        context = super().get_context_data(**kwargs)
        items = OrderItem.objects.filter(order=self.object).all()
        context["order_items"] = items
        return context
