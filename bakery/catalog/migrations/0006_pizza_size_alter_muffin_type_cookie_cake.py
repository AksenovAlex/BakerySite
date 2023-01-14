# Generated by Django 4.1.3 on 2023-01-10 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_rename_bread_type_bread_type_pie_type_pizza_muffin'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='size',
            field=models.CharField(max_length=15, null=True, verbose_name='Размер'),
        ),
        migrations.AlterField(
            model_name='muffin',
            name='type',
            field=models.CharField(max_length=100, null=True, verbose_name='Вид сдобы'),
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
    ]