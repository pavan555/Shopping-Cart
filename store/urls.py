
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductView.as_view(), name='product-list'),
    path('products/<int:product_id>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('collections/', views.CollectionView.as_view(), name='collections'),
    path('collections/<int:pk>/', views.CollectionDetailView.as_view(), name='collection-details'),
]