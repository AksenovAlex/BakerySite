import json

from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View

import random
from string import digits, ascii_lowercase

from .models import *

from random import randint


class CatalogExceptions(Exception):
    pass


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
            cart_product = {}
            product_type = {}
            for product in model.objects.all():
                if product.type not in product_type:
                    product_type[product.type] = [product]
                else:
                    product_type[product.type].append(product)

                try:
                    ct = ContentType.objects.get_for_model(model=product)
                    cp = CartProduct.objects.get(object_id=product.id, content_type=ct)
                    cart_product[product] = cp
                except:
                    cart_product[product] = None
            context = super().get_context_data(**kwargs)
            context['products'] = cart_product
            context['cart_product'] = cart_product
            context['product_type'] = product_type
            return context
        else:
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.get_categories_for_catalog()
            return context


class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            client = Client.objects.filter(user=request.user).first()
            if not client:
                client = Client.objects.create(user=request.user)
            cart = Cart.objects.filter(client=client, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(client=client)
        else:
            user = request.session.get('user')
            if user:
                us = User.objects.filter(username=user).first()
                client = Client.objects.filter(user=us.id).first()
                cart, created = Cart.objects.get_or_create(client=client)
            else:
                user_name = f'Anonimus{randint(10 ** 15, 10 ** 16)}'
                user = User.objects.create_user(username=user_name, password='None')
                client = Client.objects.create(user=user)
                cart = Cart.objects.create(client=client, for_anonymous_user=True)
                request.session['user'] = user_name

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

def get_obj_id(request):
    path_req = request.path.strip('/').split('/')
    obj_id = int(path_req[-2])
    return obj_id