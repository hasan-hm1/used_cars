from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image


class Car(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE,  related_name='car_owner')
    loves = models.ManyToManyField(User , blank=True,  related_name='car_loves')
    brand = models.CharField(max_length=15)
    model = models.CharField(max_length=15)
    production_year = models.SmallIntegerField()
    place = models.CharField(max_length=15, )
    kilometer = models.IntegerField()
    engine_capacity = models.CharField(max_length=25, )
    cylinders = models.CharField(max_length=5, )
    transmission_type = models.BooleanField()
    fuel = models.BooleanField( )
    body_shape = models.CharField(max_length=10, )
    seats = models.CharField(max_length=3, )
    technical_status = models.CharField(max_length=10, )
    outer_color = models.CharField(max_length=15, )
    inner_color = models.CharField(max_length=15, )
    extra_features = models.TextField(blank=True, null=True)
    image0 = models.ImageField(
        upload_to='cars_pics')
    image1 = models.ImageField(
        upload_to='cars_pics', blank=True, null=True)
    image2 = models.ImageField(
        upload_to='cars_pics', blank=True, null=True)
    image3 = models.ImageField(
        upload_to='cars_pics', blank=True, null=True)
    image4 = models.ImageField(
        upload_to='cars_pics', blank=True, null=True)
    image5 = models.ImageField(
        upload_to='cars_pics', blank=True, null=True)
    image6 = models.ImageField(
        upload_to='cars_pics', blank=True, null=True)
    image7 = models.ImageField(
        upload_to='cars_pics', blank=True, null=True)
    image8 = models.ImageField(
        upload_to='cars_pics', blank=True, null=True)
    image9 = models.ImageField(
        upload_to='cars_pics', blank=True, null=True)
    price = models.IntegerField(blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.brand

    # def save(self):
    #     super().save()

    #     img = Image.open(self.image0.path)
    #     output_size = (300 , 300)
    #     img.thumbnail(output_size)
    #     img.save(self.image0.path)

class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE)
    content = models.TextField()    
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content