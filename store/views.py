from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from .models import Collection, OrderItem, Product, Review
from .serializers import CollectionModelSerializer, ProductModelSerializer, ReviewModelSerializer
from .filters import ProductFilter

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer    
    lookup_field = "id"
    lookup_url_kwarg = "product_id"
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = PageNumberPagination

    # filterset_fields = ['collection_id', 'unit_price']
    
    search_fields = ['^name', 'description']
    ordering_fields = ['last_updated', 'name', 'unit_price']

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