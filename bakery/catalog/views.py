from .models import *
from .utils import *

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import DetailView, View



class BaseView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_catalog()
        products = LatestProducts.objects.get_products_for_main_page()
        context = {
            'categories': categories,
            'products': products
        }
        return render(request, 'catalog/index.html', context)


class ProductDetailView(CategoryDetailView, DetailView):

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


class CategoryDetailView(CategoryDetailView, DetailView):

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

#    model = Category
#    queryset = Category.objects.all()
#
#    context_object_name = 'category'
#    template_name = 'catalog/product_category.html'
#    slug_url_kwarg = 'slug'



def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')




