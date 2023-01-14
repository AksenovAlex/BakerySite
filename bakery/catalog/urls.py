from django.urls import path
from .views import *

urlpatterns = [
    path('', BaseView.as_view(), name='home'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='product_category'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail')
]