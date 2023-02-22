from .models import *
from .utils import *

from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.utils.safestring import mark_safe

from PIL import Image


class BreadAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(f'<span style="color:red; font-size:14px;">Загружайте изображения с разрешением не менее {Product.MIN_RESOLUTION[0]}x{Product.MIN_RESOLUTION[1]} и не более {Product.MAX_RESOLUTION[0]}x{Product.MAX_RESOLUTION[1]}</span>')

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_width, min_height = Product.MIN_RESOLUTION
        max_width, max_height = Product.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('Размер изображения не должен превышать 3МБ')
        if img.width < min_width or img.height < min_height:
            raise ValidationError('Разрешение изображения меньше минимального')
        if img.width > max_width or img.height > max_height:
            raise ValidationError('Разрешение изображения больше максимального')
        return image


class BreadAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}
    form = BreadAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='bread'))
        else:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PieAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='pie'))
        else:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PizzaAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='pizza'))
        else:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)


class MuffinAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='muffin'))
        else:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CookieAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='cookie'))
        else:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CakeAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='cake'))
        else:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CartAdmin(admin.ModelAdmin):

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            obj_id = get_obj_id(request)
            cart = Cart.objects.get(pk=obj_id)
            kwargs['queryset'] = cart.product.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)

class ClientAdmin(admin.ModelAdmin):

    def formfield_for_manytomany(self, db_field, request, **kwargs):

        if db_field.name == 'orders':
            obj_id = get_obj_id(request)
            client = Client.objects.filter(pk=obj_id).first()
            kwargs['queryset'] = Order.objects.filter(client=client.id)

            print(kwargs)
        return super().formfield_for_manytomany(db_field, request, **kwargs)



admin.site.register(Category)
admin.site.register(CartProduct)
admin.site.register(Client, ClientAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Pie, PieAdmin)
admin.site.register(Bread, BreadAdmin)
admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Muffin, MuffinAdmin)
admin.site.register(Cake, CakeAdmin)
admin.site.register(Cookie, CookieAdmin)
admin.site.register(Order)
