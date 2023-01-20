from PIL import Image

from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

User = get_user_model()


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass


class LatestProductManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        print(ct_models)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products

    @staticmethod
    def get_products_for_category(*args, **kwargs):
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all()
            print(model_products)
            products.extend(model_products)

        return products


class LatestProducts:

    objects = LatestProductManager()


class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Хлеб': 'bread__count',
        'Сдоба': 'muffin__count',
        'Пироги': 'pie__count',
        'Пицца': 'pizza__count',
        'Печенье': 'cookie__count',
        'Торты и пирожные': 'cake__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_catalog(self):
        models = get_models_for_count('bread', 'pie', 'pizza', 'muffin', 'cookie', 'cake')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.title, url=c.get_absolute_url())
            for c in qs
                ]
        return data


class Category(models.Model):

    title = models.CharField(max_length=100, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')
    objects = CategoryManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_category', kwargs={'slug':self.slug})


class Product(models.Model):

    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (1000, 1000)
    MAX_IMAGE_SIZE = 3145728

    class Meta:
        abstract = True

    title = models.CharField(max_length=150, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(verbose_name='Описание', null=True)
    structure = models.TextField(verbose_name='Состав', null=True)
    weight = models.SmallIntegerField(verbose_name='Вес')
    image = models.ImageField(upload_to="image/%Y/%m/%d", verbose_name='Изображение')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        min_width, min_height = self.MIN_RESOLUTION
        max_width, max_height = self.MAX_RESOLUTION

        if img.width < min_width or img.height < min_height:
            raise MinResolutionErrorException('Разрешение изображения меньше минимального')
        if img.width > max_width or img.height > max_height:
            raise MaxResolutionErrorException('Разрешение изображения больше максимального')
        super().save(*args, **kwargs)


class Client(models.Model):
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')
    client_name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=15, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)

    def __str__(self):
        return self.client_name


class CartProduct(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE, verbose_name='Покупатель')
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name='Корзина', related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    amount = models.PositiveIntegerField(default=1, verbose_name='Количество')
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Итоговая цена')

    def __str__(self):
        return f'Продукт {self.content_object.title} для корзины'

    def save(self, *args, **kwargs):
        self.total_price = self.amount * self.content_object.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    client = models.ForeignKey('Client', null=True, on_delete=models.PROTECT, verbose_name='Покупатель')
    product = models.ManyToManyField(CartProduct, blank=True, related_name='related_carts')
    amount = models.PositiveIntegerField(default=1, verbose_name='Количество')
    total_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Итоговая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        cart_data = self.product.aggregate(models.Sum('total_price'), models.Count('id'))
        print(cart_data)
        if cart_data.get('total_price__sum'):
            self.total_price = cart_data['total_price__sum']
        else:
            self.total_price = 0
        self.total_product = cart_data['id__count']
        super().save(*args, **kwargs)


#class OrderStatus(models.Model):
#    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
#    status_name = models.CharField(max_length=15, verbose_name='Состояние заказа')


#class Order(models.Model):
#    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')
#    client = models.ForeignKey('Client', on_delete=models.PROTECT, verbose_name='Покупатель')
#    status = models.ForeignKey('OrderStatus', on_delete=models.PROTECT, verbose_name='Состояние заказа')

# Create your models here.

class Pie(Product):

    type = models.CharField(max_length=100, null=True, verbose_name='Вид пирога')
    fill = models.CharField(max_length=100, verbose_name='Начинка')
    size = models.CharField(max_length=15, verbose_name='Размер')

    def __str__(self):
        return f'{self.category.title}: {self.title}'

    def get_absolut_url(self):
        return get_product_url(self, 'product_detail')


class Bread(Product):

    type = models.CharField(max_length=100, verbose_name='Вид хлеба')

    def __str__(self):
        return f'{self.category.title}: {self.title}'

    def get_absolut_url(self):
        return get_product_url(self, 'product_detail')


class Pizza(Product):

    type = models.CharField(max_length=100, null=True, verbose_name='Вид пиццы')
    size = models.CharField(max_length=15, null=True, verbose_name='Размер')

    def __str__(self):
        return f'{self.category.title}: {self.title}'

    def get_absolut_url(self):
        return get_product_url(self, 'product_detail')


class Muffin(Product):

    type = models.CharField(max_length=100, null=True, verbose_name='Вид сдобы')

    def __str__(self):
        return f'{self.category.title}: {self.title}'

    def get_absolut_url(self):
        return get_product_url(self, 'product_detail')


class Cookie(Product):

    type = models.CharField(max_length=100, null=True, verbose_name='Вид печенья')

    def __str__(self):
        return f'{self.category.title}: {self.title}'

    def get_absolut_url(self):
        return get_product_url(self, 'product_detail')


class Cake(Product):

    type = models.CharField(max_length=100, null=True, verbose_name='Вид пирожного')

    def __str__(self):
        return f'{self.category.title}: {self.title}'

    def get_absolut_url(self):
        return get_product_url(self, 'product_detail')