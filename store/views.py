from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer, ProductModelSerializer


# Create your views here.

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'POST':
        serializer = ProductModelSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        query_set = Product.objects.select_related('collection').all()
        serializer = ProductModelSerializer(query_set, many=True, context={'request': request})
        return Response(serializer.data)

@api_view(["GET", "PUT", "PATCH"])
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method=="GET":
        serializer = ProductModelSerializer(product)
    elif request.method=="PUT":
        serializer = ProductModelSerializer(product, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    elif request.method=="PATCH":
        serializer = ProductModelSerializer(product, data = request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(product, serializer.validated_data)
    return Response(serializer.data)

@api_view()
def get_collection_details(request, pk):
    return Response(f"Details of collection with id: {pk}")