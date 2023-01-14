from django.views.generic.detail import SingleObjectMixin

from .models import *


class CategoryDetailView(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.get_categories_for_catalog()
        return context