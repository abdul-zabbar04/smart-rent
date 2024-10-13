from rest_framework import serializers
from filterings.models import Category, District

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields= '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model= District
        fields= '__all__'