from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.pagination import PageNumberPagination

from .permissions import CustomerHistoryDjangoPermission, IsAdminOrReadOnly
from .models import Cart, CartItem, Collection, Customer, Order, OrderItem, Product, Review
from .serializers import (
    AddCartItemSerializer,
    CartItemSerializer,
    CartSerializer,
    CollectionModelSerializer,
    CreateOrderSerializer,
    CustomerSerializer,
    OrderSerializer,
    ProductModelSerializer,
    ReviewModelSerializer,
    UpdateCartItemSerializer,
)
from .filters import ProductFilter


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    lookup_field = "id"
    lookup_url_kwarg = "product_id"
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]

    # filterset_fields = ['collection_id', 'unit_price']

    search_fields = ["^name", "description"]
    ordering_fields = ["last_updated", "name", "unit_price"]

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs["product_id"]).count() > 0:
            return Response(
                {
                    "error": "Product can't be deleted because it is associated with one or more order items."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all().annotate(products_count=Count("products"))
    serializer_class = CollectionModelSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": "Collection can't be deleted because it includes one or more products."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewModelSerializer

    def get_queryset(self):
        product_id = self.kwargs["product_product_id"]
        return Review.objects.filter(product_id=product_id)

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_product_id"]}


class CreateRetrieveDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    pass


class CreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    A viewset that provides default `create()`, `destroy()` actions.
    """

    pass



class CartViewSet(CreateRetrieveDeleteViewSet):
    queryset = Cart.objects.prefetch_related("items__product").all()
    serializer_class = CartSerializer



class CartItemViewSet(CreateDestroyViewSet):
    http_method_names = ["get", "post", "patch", "delete"] #To only allow these methods

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        if self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        cart_id = self.kwargs["cart_pk"]
        return CartItem.objects.select_related("product").filter(cart_id=cart_id)

    def get_serializer_context(self):
        return {"cart_pk": self.kwargs["cart_pk"]}


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, permission_classes=[CustomerHistoryDjangoPermission])
    def history(self, request, pk):
        return Response(f"This is customer {pk} history API")

    @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def me(self, request):
        userid = request.user.id
        (customer, _created) = Customer.objects.get_or_create(user_id = userid)
        print("Customer:", customer)
        if request.method == "GET":
            serializer = CustomerSerializer(customer)
        elif request.method == "PUT":
            serializer = CustomerSerializer(customer, data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data = request.data, context = {"user_id": self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.select_related("customer").prefetch_related("items__product").all()
        user = self.request.user
        if user.is_staff:
            return queryset
        try:
            customer_id = Customer.objects.only("id").get(user_id=user.id)
        except Customer.DoesNotExist:
            return Order.objects.none()
        return queryset.filter(customer_id=customer_id)