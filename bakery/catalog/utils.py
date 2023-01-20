from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View

from .models import *


class CategoryDetailMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.get_categories_for_catalog()
        return context


class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            client = Client.objects.filter(client_name=request.user).first()
            if not client:
                client = Client.objects.create(client_name=request.user)
            cart = Cart.objects.filter(client=client, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(client=client)
        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)