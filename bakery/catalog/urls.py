from django.urls import path
from .views import *

urlpatterns = [
    path('', BaseView.as_view(), name='home'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='product_category'),
    path('category/<str:ct_model>/<str:type>/', TypeProductsView.as_view(), name='type_products'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(), name="add_to_cart"),
    path('remove-from-cart/<str:ct_model>/<str:slug>/', DeleteFromCartView.as_view(), name="delete_from_cart"),
    path('change-amount/<str:ct_model>/<str:slug>/', ChangeAmountView.as_view(), name="change_amount"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('make-order/', MakeOrderView.as_view(), name="make_order"),
    path('register/', RegisterUser.as_view(), name="register"),
    path('login/', LoginClient.as_view(), name="login"),
    path('logout/', logout_user, name="logout"),
]