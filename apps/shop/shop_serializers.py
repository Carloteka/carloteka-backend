from rest_framework import serializers

from .models import CategoryModel, CategoryImageModel


class CategoryImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField

    class Meta:
        model = CategoryImageModel
        fields = ['image']


class CategorySerializer(serializers.ModelSerializer):
    images = CategoryImageSerializer(many=True)

    class Meta:
        model = CategoryModel
        fields = ['id', 'id_name', 'name', 'description', 'images']
