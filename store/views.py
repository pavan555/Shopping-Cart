from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Collection, Product
from .serializers import CollectionModelSerializer, ProductModelSerializer


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

@api_view(["GET", "PUT", "PATCH", "DELETE"])
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method=="DELETE":
        if product.orderitems.count() > 0:
            return Response({"error": "Product can't be deleted because it is associated with one or more order items."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
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



@api_view(['GET', 'POST'])
def get_collections(request):
    if request.method == "POST":
        serializer = CollectionModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == "GET":
        query_set = Collection.objects.all().annotate(products_count=Count('products'))
        serializer = CollectionModelSerializer(query_set, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def get_collection_details(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
    if request.method == "DELETE":
        if collection.products_count > 0:
            return Response({"error": "Collection can't be deleted because it includes one or more products."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == "GET":
        serializer = CollectionModelSerializer(collection)
    elif request.method == "PUT":
        serializer = CollectionModelSerializer(collection, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    elif request.method == "PATCH":
        serializer = CollectionModelSerializer(collection, data = request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    return Response(serializer.data)