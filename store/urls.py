
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from pprint import pprint
from . import views

router = DefaultRouter()
router.register('products', viewset=views.ProductViewSet, basename='product')
router.register('collections', viewset=views.CollectionViewSet, basename='collection')
# pprint(router.urls)  # For debugging purposes to see the generated URL patterns

urlpatterns = router.urls

# urlpatterns = [
    # path('', include(router.urls))
    # path('products/', views.ProductView.as_view(), name='product-list'),
    # path('products/<int:product_id>/', views.ProductDetailView.as_view(), name='product-detail'),
    # path('collections/', views.CollectionView.as_view(), name='collections'),
    # path('collections/<int:pk>/', views.CollectionDetailView.as_view(), name='collection-details'),
# ]