from rest_framework import serializers
from .models import Order, OrderItem
from product.serializers import ProductSeriallizers

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model =OrderItem
        fields = (
            'price',
            'product',
            'quantity'
        )

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = (
            "id",
            "name",
            "email",
            "address",
            "zipcode",
            "phone",
            "items"
        )
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order