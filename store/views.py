from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from .models import Collection, OrderItem, Product, Review
from .serializers import CollectionModelSerializer, ProductModelSerializer, ReviewModelSerializer


class ProductViewSet(ModelViewSet):
    # queryset = Product.objects.all()
    serializer_class = ProductModelSerializer    
    lookup_field = "id"
    lookup_url_kwarg = "product_id"

    def get_queryset(self):
        queryset = Product.objects.all()
        collection_id = self.request.query_params.get("collection_id")
        if collection_id is not None:
            queryset = queryset.filter(collection_id=collection_id)
        return queryset

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['product_id']).count() > 0:
            return Response({"error": "Product can't be deleted because it is associated with one or more order items."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all().annotate(products_count=Count('products'))
    serializer_class = CollectionModelSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({"error": "Collection can't be deleted because it includes one or more products."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewModelSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_product_id']
        return Review.objects.filter(product_id=product_id)

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_product_id']}