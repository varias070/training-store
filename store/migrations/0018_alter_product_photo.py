# Generated by Django 3.2.5 on 2021-08-06 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_alter_order_сustomer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(upload_to='img', verbose_name='Фото'),
        ),
    ]
