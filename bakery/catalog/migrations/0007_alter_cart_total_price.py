# Generated by Django 4.1.3 on 2023-01-20 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_pizza_size_alter_muffin_type_cookie_cake'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Итоговая цена'),
        ),
    ]