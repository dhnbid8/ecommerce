from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import Profile
from account import models
from product.serializers import ProductSeriallizers
from product.models import Product
from rest_framework.decorators import api_view
from .serializers import ProfileSerializers
from  order.models import Order
from order.serializers import OrderSerializer

class likesProducts(APIView):
    def get(self, request):
        profile = models.Profile.objects.get(user=request.user) if Profile.objects.filter(user=request.user) else Profile.objects.create(user=request.user) 
        
        products = profile.likes_products
        serializer = ProductSeriallizers(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        profile = Profile.objects.get(user=request.user) if Profile.objects.filter(user=request.user).count() > 0 else Profile.objects.create(user=request.user) 
        products = profile.likes_products
        try:
            product = Product.objects.get(id=request.data['product'])
            if product in products.all():
                return Response({"msg":"محصول در لیتس علاقه مندی ها وجود دارد "})

            products.add(
                product
            )
            return Response({"msg":"محصول با موفقیت اضافه شد"})

        except :
            return Response({"msg":"محصول یافت نشد "})
    
@api_view(['DELETE'])
def delete(request, id):
    
    profile = Profile.objects.get(user=request.user) if Profile.objects.filter(user=request.user).count() > 0 else Profile.objects.create(user=request.user) 
    products = profile.likes_products
    product = Product.objects.get(id=1)
    # try:
    if not product in products.all():
        return Response({"msg":"محصول در لیست علاقه مندی ها نمی باشد"})
    elif product in products.all():
        products.remove(
            product
            )
        return Response({"msg":"محصول با موفقیت حذف شد"})

    # except :
    #     return Response({"msg":"محصول یافت نشد "})

class ProfileViwe(APIView):
    
    def get(self, request):
        profile = request.user.Profile if Profile.objects.filter(user=request.user).count() > 0 else Profile.objects.create(user=request.user)
        serializers = ProfileSerializers(profile)
        return Response(serializers.data)

    def post(self, request):
        profile = request.user.Profile if Profile.objects.filter(user=request.user).count() > 0 else Profile.objects.create(user=request.user)
        
        # context = {}
        if request.data['name'] != None:
            profile.name = request.data['name']


        if request.data['phonenumber'] != None:
            profile.phonenumber = request.data['phonenumber']
        
        if request.data['address'] != None:
            profile.address = request.data['address']

        if request.data['zipcode'] != None:
            profile.zipcode = request.data['zipcode']
        
        profile.save()
        serializers = ProfileSerializers(profile)
        return Response({"msg":"با موفقیت اضافه شد "})


# {
#     "name": "دانیال",
#     "phonenumber": "0933452151",
#     "address": "تهران .",
#     "zipcode": "45251752"
# }

@api_view(['GET'])
def myOrders(request):
    myOrders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(myOrders)
    return Response(serializer.data)