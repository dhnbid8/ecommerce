from django.shortcuts import render
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.permissions import IsAuthenticated


from rest_framework import status, authentication, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Card, CardItem
from .serializers import CardSerializer, CardItemSerializer
from rest_framework.response import Response
from product.models import Product
from product.serializers import ProductSeriallizers


import logging
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException

@api_view(["GET"])
def get(request):
	print(request.user.id)
	card = Card.objects.filter(user=request.user).first() if Card.objects.filter(user=request.user).count() > 0 else Card.objects.create(user=request.user).save()

	serializer = CardSerializer(card)
	return Response(serializer.data)
	
@api_view(["POST"])
def addItemToCard(request):

	user = request.user

	if Product.objects.filter(id=request.data['product']).count() > 0 : 
		product = Product.objects.get(id=request.data['product'])
	else :
		return Response({"msg":"محصول مورد نظر یافت نشد !"})

	quantity = request.data['quantity']

	card = Card.objects.filter(user=request.user).first() if Card.objects.filter(user=request.user).count() > 0 else Card.objects.create(user=request.user).save()
	
	if card.product_exists(product):
		
		item = CardItem.objects.get(id=card.get_exists_product(product).id)
		item.quantity += quantity
		item.save()
		return Response({"msg":"تعداد محصول با موفقیت اضافه شد !"})
		
	else :

		items = card.items.all()
		card.items.create(product=product, quantity=quantity)
		return Response({"msg":"محصول با موفقیت اضافه شد "})

	return Response({"msg":"محصول مورد نظر یافت نشد !"})
	


"""
{
"product":1,
"quantity":1
}
"""

@api_view(['DELETE'])
def deleteItem(request, id):
	
	if CardItem.objects.filter(id=id).count() > 0:
		CardItem.objects.filter(id=id).first().delete()
		
		return Response({"msg":"محصول با موفقیت از سبد خرید حذف شد!"})
	else:
		return Response({"msg":"محصول با این شناسه یافت نشد !"})
