
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='Product List'),
    path('products/<int:product_id>/', views.product_detail, name='Product Detail'),
]