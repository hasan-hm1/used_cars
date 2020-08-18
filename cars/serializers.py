from rest_framework import serializers
from .models import Car

class CarSerializer(serializers.ModelSerializer):


    class Meta:
        model = Car
        fields = ('brand' , 'model' , 'production_year')
        fields = '__all__'