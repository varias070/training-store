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
    photo = models.ImageField(upload_to='static/img', null=True, verbose_name='Фото')
    type = models.ForeignKey('Type', null=True, on_delete=models.CASCADE, verbose_name='Тип')
    description = models.TextField(null=True, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Manufacturer(models.Model):
    title = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class Type(models.Model):
    title = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Order(models.Model):
    сustomer = models.ForeignKey(User, null=True, on_delete=models.CASCADE,)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE,)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE,)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = 'Заказаный товар'
        verbose_name_plural = 'Заказаные товары'