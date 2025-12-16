
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('products/<int:product_id>/', views.product_detail, name='product-detail'),
    path('collections/', views.get_collections, name='collections'),
    path('collections/<int:pk>/', views.get_collection_details, name='collection-details'),
]