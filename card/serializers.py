from rest_framework import serializers
from card.models import Card, CardItem
from product.serializers import ProductSeriallizers

class CardItemSerializer(serializers.ModelSerializer):
	product = ProductSeriallizers()
	class Meta:
		model = CardItem
		fields = (
			'id',
			'product',
			'quantity'
			)

class CardSerializer(serializers.ModelSerializer):
	items = CardItemSerializer(many=True)
	class Meta:
		model = Card
		fields = (
			'id',
			'items',
			'get_items_price'
			)

