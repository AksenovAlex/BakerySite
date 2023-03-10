from django import views

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .models import *
from .utils import *
from .forms import OrderForm, LoginClientForm, RegistrationForm

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import DetailView, View, CreateView
from django.contrib import messages
from django.db import transaction


class BaseView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_catalog()
        context = {
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'catalog/index.html', context)


class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'catalog/product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        product_object = kwargs['object']
        ct = ContentType.objects.get(model=self.model._meta.model_name)
        context = super().get_context_data(**kwargs)
        try:
            cart_product = CartProduct.objects.get(object_id=product_object.id, content_type=ct)
            context['all_cart_products'] = self.cart.product.all()
            context['cart_product'] = cart_product
        except:
            pass
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'catalog/product_category.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        context['all_cart_products'] = self.cart.product.all()
        return context


class TypeProductsView(CartMixin, CategoryDetailMixin, DetailView):

    def get(self, request, *args, **kwargs):
        ct_model, type = kwargs['ct_model'], kwargs['type']
        model = self.CT_MODEL_MODEL_CLASS[ct_model]
        category = Category.objects.get(slug=ct_model)
        cart_product = {}
        product_type = {}
        for prod_type in model.objects.all():
            if prod_type.type not in product_type:
                product_type[prod_type.type] = [prod_type]
            else:
                product_type[prod_type.type].append(prod_type)

        for product in model.objects.filter(type=type):
            try:
                ct = ContentType.objects.get_for_model(model=product)
                cp = CartProduct.objects.get(object_id=product.id, content_type=ct)
                cart_product[product] = cp
            except:
                cart_product[product] = None

        all_cart_products = self.cart.product.all()

        context = {
            'category': category,
            'category_type': type,
            'products': cart_product,
            'product_type': product_type,
            'all_cart_products': all_cart_products,
            'cart': self.cart
        }

        return render(request, 'catalog/product_category.html', context)


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_catalog()
        context = {
            'categories': categories,
            'cart': self.cart
        }
        return render(request, 'catalog/cart.html', context)


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_catalog()
        form = OrderForm(request.POST or None)
        context = {
            'categories': categories,
            'cart': self.cart,
            'form': form
        }
        return render(request, 'catalog/checkout.html', context)


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
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, '?????????? ?????????????? ????????????????')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs['ct_model'], kwargs['slug']
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            client=self.cart.client, cart=self.cart,
            content_type=content_type,
            object_id=product.id
        )
        self.cart.product.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, '?????????? ?????????????? ????????????')
        return HttpResponseRedirect('/cart/')


class ChangeAmountView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs['ct_model'], kwargs['slug']
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            client=self.cart.client, cart=self.cart,
            content_type=content_type,
            object_id=product.id
        )
        amount = int(request.POST.get('amount'))
        cart_product.amount = amount
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, '???????????????????? ?????????????? ????????????????')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        if request.user.is_authenticated:
            client = Client.objects.filter(user=request.user).first()
        else:
            user_name = request.session.get('user')
            user = User.objects.filter(username=user_name).first()
            client = Client.objects.filter(user=user.id).first()
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.client = client
            new_order.first_name = form.cleaned_data['first_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            new_order.cart = self.cart
            new_order.save()
            client.orders.add(new_order)
            messages.add_message(request, messages.INFO, '?????????????? ???? ??????????!')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class LoginClient(LoginView):
    form_class = LoginClientForm
    template_name = 'catalog/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterUser(views.View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'catalog/register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Client.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'catalog/register.html', context)



def logout_user(request):
    logout(request)
    return redirect('home')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>???????????????? ???? ??????????????</h1>')
