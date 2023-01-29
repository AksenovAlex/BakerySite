from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View

from .models import *


class CategoryDetailMixin(SingleObjectMixin):

    CT_MODEL_MODEL_CLASS = {
        'bread': Bread,
        'pie': Pie,
        'pizza': Pizza,
        'muffin': Muffin,
        'cookie': Cookie,
        'cake': Cake,
    }

    def get_context_data(self, **kwargs):
        if isinstance(self.get_object(), Category):
            model = self.CT_MODEL_MODEL_CLASS[self.get_object().slug]
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.get_categories_for_catalog()
            context['category_products'] = model.objects.all()
            return context
        else:
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
        self.cart.save()
        return super().dispatch(request, *args, **kwargs)


def recalc_cart(cart):
    cart_data = cart.product.aggregate(models.Sum('total_price'), models.Count('id'))
    if cart_data.get('total_price__sum'):
        cart.total_price = cart_data['total_price__sum']
    else:
        cart.total_price = 0
    cart.total_product = cart_data['id__count']
    cart.save()