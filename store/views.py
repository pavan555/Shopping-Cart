from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin

from .models import Collection, Product
from .serializers import CollectionModelSerializer, ProductModelSerializer


# Create your views here.
class ProductView(APIView, ListModelMixin, CreateModelMixin):
    def get_queryset(self):
        return Product.objects.select_related('collection').all()
    
    def filter_queryset(self, queryset):
        return queryset
    
    def paginate_queryset(self, queryset):
        return None
    
    def get_serializer(self, *args, **kwargs):
        return ProductModelSerializer(*args, **kwargs)
    
    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)

class ProductDetailView(APIView):

    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        serializer = ProductModelSerializer(product)
        return Response(serializer.data)
    
    def delete(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        if product.orderitems.count() > 0:
            return Response({"error": "Product can't be deleted because it is associated with one or more order items."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        serializer = ProductModelSerializer(product, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        serializer = ProductModelSerializer(product, data = request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(product, serializer.validated_data)
        return Response(serializer.data)


class CollectionView(APIView):
    def post(self, request):
        serializer = CollectionModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        query_set = Collection.objects.all().annotate(products_count=Count('products'))
        serializer = CollectionModelSerializer(query_set, many=True)
        return Response(serializer.data)

class CollectionDetailView(APIView):
    def get(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
        serializer = CollectionModelSerializer(collection)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
        if collection.products_count > 0:
            return Response({"error": "Collection can't be deleted because it includes one or more products."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
        serializer = CollectionModelSerializer(collection, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def patch(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
        serializer = CollectionModelSerializer(collection, data = request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)