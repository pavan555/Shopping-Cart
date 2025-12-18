
from django.urls import path, include
from rest_framework_nested.routers import NestedSimpleRouter, SimpleRouter, DefaultRouter
# from rest_framework.routers import DefaultRouter
from pprint import pprint
from . import views

router = DefaultRouter()
router.register('products', viewset=views.ProductViewSet, basename='product')
router.register('collections', viewset=views.CollectionViewSet, basename='collection')
router.register('carts', viewset=views.CartViewSet, basename='cart')
router.register('customers', viewset=views.CustomerViewSet, basename='customers')


products_router = NestedSimpleRouter(router, 'products', lookup="product")
products_router.register('reviews', viewset=views.ReviewViewSet, basename='product-reviews')

carts_router = NestedSimpleRouter(router, 'carts', lookup="cart")
carts_router.register('items', viewset=views.CartItemViewSet, basename='product-reviews')
# pprint(router.urls)
# pprint(reviews_router.urls)  # For debugging purposes to see the generated URL patterns

# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('', include(carts_router.urls))
    # path('products/', views.ProductView.as_view(), name='product-list'),
    # path('products/<int:product_id>/', views.ProductDetailView.as_view(), name='product-detail'),
    # path('collections/', views.CollectionView.as_view(), name='collections'),
    # path('collections/<int:pk>/', views.CollectionDetailView.as_view(), name='collection-details'),
]