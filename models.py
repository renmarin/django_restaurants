from django.db import models

# Create your models here.


class Restaurant(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'


class MenuItem(models.Model):
    name = models.CharField(max_length=70)
    description = models.CharField(max_length=300)
    price = models.CharField(max_length=8)
    course = models.CharField(max_length=10)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f'''{self.name} {self.description} {self.price}'''
