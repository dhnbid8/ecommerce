from django.db.models import Q
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Category
from .serializers import ProductSeriallizers, CategorySeriallizers

class LastesProductsList(APIView):
    
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        print(products)
        serializer = ProductSeriallizers(products, many=True)
        return Response(serializer.data)

class ProductDetail(APIView):
    def get_object(self, product_slug):
        try:
            return Product.objects.filter(slug=product_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, request, product_slug, format=None):
        product = self.get_object(product_slug)
        serializer = ProductSeriallizers(product)

        return Response(serializer.data)

class CategoryDatail(APIView):
    
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySeriallizers(category)

        return Response(serializer.data)

@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSeriallizers(products, many=True)
        return Response(serializer.data)
    else:
        return Response([])