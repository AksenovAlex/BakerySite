from .models import *
from .utils import *

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, View



class BaseView(CartMixin, View):

    def get(self, request, *args, **kwargs):

        categories = Category.objects.get_categories_for_catalog()
        products = LatestProducts.objects.get_products_for_main_page()
        context = {
            'categories': categories,
            'products': products,
            'cart': self.cart
        }
        return render(request, 'catalog/index.html', context)


class ProductDetailView(CategoryDetailMixin, DetailView):

    CT_MODEL_MODEL_CLASS = {
        'bread': Bread,
        'pie': Pie,
        'pizza': Pizza,
        'muffin': Muffin,
        'cookie': Cookie,
        'cake': Cake,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'catalog/product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        return context


class CategoryDetailView(CategoryDetailMixin, DetailView):

    def get(self, request, *args, **kwargs):
        category = Category.objects.get(slug=kwargs['slug'])
        products = LatestProducts.objects.get_products_for_category(kwargs['slug'])
        types = list(set(prod.type for prod in products))

        context = {
            'category': category,
            'products': products,
            'types': types,
        }
        print(context)
        return render(request, 'catalog/product_category.html', context)


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_catalog()
        context = {
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'catalog/cart.html', context)


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs['ct_model'], kwargs['slug']
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            client=self.cart.client, cart=self.cart, content_type=content_type,
            object_id=product.id
        )
        if created:
            self.cart.product.add(cart_product)
        self.cart.save()
        return HttpResponseRedirect('/cart/')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')




