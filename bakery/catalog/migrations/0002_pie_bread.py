# Generated by Django 4.1.3 on 2022-12-22 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
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
                ('fill', models.CharField(max_length=100, verbose_name='Начинка')),
                ('size', models.CharField(max_length=15, verbose_name='Размер')),
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
                ('bread_type', models.CharField(max_length=100, verbose_name='Вид хлеба')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='Категория')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
