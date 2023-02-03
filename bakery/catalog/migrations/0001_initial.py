# Generated by Django 4.1.3 on 2023-01-30 16:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=0, verbose_name='Количество')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Итоговая цена')),
                ('in_order', models.BooleanField(default=False)),
                ('for_anonymous_user', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100, verbose_name='Название')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Номер телефона')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес')),
            ],
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=150, verbose_name='Название')),
                ('slug', models.SlugField(max_length=150, unique=True, verbose_name='URL')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('structure', models.TextField(null=True, verbose_name='Состав')),
                ('weight', models.SmallIntegerField(verbose_name='Вес')),
                ('image', models.ImageField(upload_to='image/%Y/%m/%d', verbose_name='Изображение')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('type', models.CharField(max_length=100, null=True, verbose_name='Вид пиццы')),
                ('size', models.CharField(max_length=15, null=True, verbose_name='Размер')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='Категория')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=150, verbose_name='Название')),
                ('slug', models.SlugField(max_length=150, unique=True, verbose_name='URL')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('structure', models.TextField(null=True, verbose_name='Состав')),
                ('weight', models.SmallIntegerField(verbose_name='Вес')),
                ('image', models.ImageField(upload_to='image/%Y/%m/%d', verbose_name='Изображение')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('type', models.CharField(max_length=100, null=True, verbose_name='Вид пирога')),
                ('fill', models.CharField(max_length=100, verbose_name='Начинка')),
                ('size', models.CharField(max_length=15, verbose_name='Размер')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='Категория')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('address', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Адрес')),
                ('status', models.CharField(choices=[('new', 'Новый заказ'), ('in_progress', 'Заказ в обработке'), ('is_ready', 'Заказ готов'), ('completed', 'Заказ выполнен')], default='new', max_length=100, verbose_name='Состояние заказа')),
                ('buying_type', models.CharField(choices=[('self', 'Самовывоз'), ('delivery', 'Доставка')], default='delivery', max_length=100, verbose_name='Тип заказа')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий к заказу')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')),
                ('order_date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата получения заказа')),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.cart', verbose_name='Корзина')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_orders', to='catalog.client', verbose_name='Покупатель')),
            ],
        ),
        migrations.CreateModel(
            name='Muffin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=150, verbose_name='Название')),
                ('slug', models.SlugField(max_length=150, unique=True, verbose_name='URL')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('structure', models.TextField(null=True, verbose_name='Состав')),
                ('weight', models.SmallIntegerField(verbose_name='Вес')),
                ('image', models.ImageField(upload_to='image/%Y/%m/%d', verbose_name='Изображение')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('type', models.CharField(max_length=100, null=True, verbose_name='Вид сдобы')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='Категория')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cookie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=150, verbose_name='Название')),
                ('slug', models.SlugField(max_length=150, unique=True, verbose_name='URL')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('structure', models.TextField(null=True, verbose_name='Состав')),
                ('weight', models.SmallIntegerField(verbose_name='Вес')),
                ('image', models.ImageField(upload_to='image/%Y/%m/%d', verbose_name='Изображение')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('type', models.CharField(max_length=100, null=True, verbose_name='Вид печенья')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='Категория')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='client',
            name='orders',
            field=models.ManyToManyField(related_name='related_client', to='catalog.order', verbose_name='Заказы покупателя'),
        ),
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('amount', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Итоговая цена')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_products', to='catalog.cart', verbose_name='Корзина')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.client', verbose_name='Покупатель')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.client', verbose_name='Покупатель'),
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ManyToManyField(blank=True, related_name='related_carts', to='catalog.cartproduct'),
        ),
        migrations.CreateModel(
            name='Cake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=150, verbose_name='Название')),
                ('slug', models.SlugField(max_length=150, unique=True, verbose_name='URL')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('structure', models.TextField(null=True, verbose_name='Состав')),
                ('weight', models.SmallIntegerField(verbose_name='Вес')),
                ('image', models.ImageField(upload_to='image/%Y/%m/%d', verbose_name='Изображение')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('type', models.CharField(max_length=100, null=True, verbose_name='Вид пирожного')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='Категория')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Bread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=150, verbose_name='Название')),
                ('slug', models.SlugField(max_length=150, unique=True, verbose_name='URL')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('structure', models.TextField(null=True, verbose_name='Состав')),
                ('weight', models.SmallIntegerField(verbose_name='Вес')),
                ('image', models.ImageField(upload_to='image/%Y/%m/%d', verbose_name='Изображение')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('type', models.CharField(max_length=100, verbose_name='Вид хлеба')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='Категория')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
