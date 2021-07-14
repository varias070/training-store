from django.db import models


class Product(models.Model):
    title = models.CharField(null=True, max_length=50)
    manufacturer = models.ForeignKey('Manufacturer', null=True, on_delete=models.CASCADE,)
    price = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    mass = models.IntegerField(default=0)
    type = models.CharField(null=True, max_length=50)


    def publish(self):
        self.save()

    def __str__(self):
        return self.title


class Manufacturer(models.Model):
    title = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.title



