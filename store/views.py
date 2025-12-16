from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Collection, Product
from .serializers import CollectionModelSerializer, ProductModelSerializer


# Create your views here.
class ProductView(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductModelSerializer


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    lookup_field = "id"
    lookup_url_kwarg = "product_id"

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        if product.orderitems.count() > 0:
            return Response({"error": "Product can't be deleted because it is associated with one or more order items."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return self.destroy(request, *args, **kwargs)

    
class CollectionView(ListCreateAPIView):
    queryset = Collection.objects.all().annotate(products_count=Count('products'))
    serializer_class = CollectionModelSerializer


class CollectionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionModelSerializer
    
    def delete(self, request, *args, **kwargs):
        collection = self.get_object()
        if collection.products_count > 0:
            return Response({"error": "Collection can't be deleted because it includes one or more products."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return self.destroy(request, *args, **kwargs)