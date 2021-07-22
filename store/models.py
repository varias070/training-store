from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    objects = None
    title = models.CharField(null=True, max_length=50)
    manufacturer = models.ForeignKey('Manufacturer', null=True, on_delete=models.CASCADE,)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    mass = models.IntegerField(default=0)
    type = models.CharField(null=True, max_length=50)

    def publish(self):
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        index_together = (('id'),)


class Manufacturer(models.Model):
    title = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.title


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
