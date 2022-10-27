from django.db import models
from django.contrib.auth.models import User
from  product.models import Product
from decimal import Decimal
from order.models import OrderItem, Order

class CardItem(models.Model):
	product = models.ForeignKey(Product, related_name="CartItem", on_delete=models.CASCADE)
	quantity = models.IntegerField()

	def __str__(self):
		return self.product.name
	
	def convert_to_order_item(self, order):
		return order.items.create(product=self.product, quantity=self.quantity)

class Card(models.Model):
	user = models.OneToOneField(User, related_name="Card", on_delete=models.CASCADE, unique=True)
	items = models.ManyToManyField(CardItem,  default=[])
	timestamp = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.username

	def get_items_price(self):
		amount = 0
		amount = Decimal(amount)

		if self.items:
			for item in self.items.all() :
				amount += item.product.price * item.quantity

		return amount

	def product_exists(self, product):
		for item in self.items.all():
			if item.product == product:
				return True
		return False
	
	def get_exists_product(self, product):
		for item in self.items.all():
			if item.product == product:
				return item
		return null
	
	def convert_to_order(self, name, address, phoneNum, zipcode):
		order = Order.objects.create(user=self.user, name=name, address=address, zipcode=zipcode, phone=phoneNum, paid_amount=self.get_items_price())
		for item in self.items.all():
			item.convert_to_order_item(order)
			item.delete()
		