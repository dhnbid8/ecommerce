from rest_framework import serializers

from .models import Category, Product

class ProductSeriallizers(serializers.ModelSerializer):

    class Meta:
        model =  Product
        fields = (
            'id',
            'name',
            'get_absolute_url',
            'description',
            'price',
            'get_image',
            'get_thumbnail',
            'get_category_name',
            'get_category_slug'
        )

class CategorySeriallizers(serializers.ModelSerializer):
    products = ProductSeriallizers(many=True)

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'get_absolute_url',
            'products'
        )