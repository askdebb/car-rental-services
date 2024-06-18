from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=100)
    make = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Image(models.Model):
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='car_images')

    def __str__(self):
        return f"Image of {self.car.name}"
