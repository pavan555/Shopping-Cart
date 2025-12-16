from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer, ProductModelSerializer


# Create your views here.

@api_view()
def product_list(request):
    query_set = Product.objects.select_related('collection').all()
    serializer = ProductModelSerializer(query_set, many=True, context={'request': request})
    return Response(serializer.data)

@api_view()
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    serializer = ProductModelSerializer(product, context = {'request': request})
    return Response(serializer.data)

@api_view()
def get_collection_details(request, pk):
    return Response(f"Details of collection with id: {pk}")