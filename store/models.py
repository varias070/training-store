from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    objects = None
    title = models.CharField(null=True, max_length=50, verbose_name='Название')
    manufacturer = models.ForeignKey('Manufacturer', null=True, on_delete=models.CASCADE, verbose_name='Проиводитель')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    height = models.IntegerField(default=0, verbose_name='Высота')
    width = models.IntegerField(default=0, verbose_name='Ширина')
    mass = models.IntegerField(default=0, verbose_name='Масса')
    photo = models.ImageField(upload_to='img', verbose_name='Фото')
    type = models.ForeignKey('Type', null=True, on_delete=models.CASCADE, verbose_name='Тип')
    description = models.TextField(null=True, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Manufacturer(models.Model):
    title = models.CharField(max_length=50, null=True, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class Type(models.Model):
    title = models.CharField(max_length=50, null=True, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'



