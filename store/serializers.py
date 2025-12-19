
from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import Cart, CartItem, Customer, Order, OrderItem, Product, Collection, Review
from .signals import order_created


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True)
    price = serializers.DecimalField(max_digits=5, decimal_places=2, source='unit_price')
    discount_price = serializers.SerializerMethodField(method_name="calculate_discounted_price")

    collectionSerializer = CollectionSerializer(source='collection', read_only=True)
    collectionString = serializers.CharField(source='collection', read_only=True)
    collectionPkKey = serializers.PrimaryKeyRelatedField(source='collection', read_only=True)

    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='collection-detail'
    )

    def calculate_discounted_price(self, obj: Product):
        if obj.unit_price > 9:
            return obj.unit_price * Decimal(0.9)  # 10% discount
        return obj.unit_price



class CollectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
    
    products_count = serializers.IntegerField(required=False, read_only=True) 
    # required=False or read_only=True because it's an annotated field, not a model field
    
    

class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'slug', 'inventory', 'unit_price', 'discounted_price', 'collection']
    
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-details'
    # )

    discounted_price = serializers.SerializerMethodField(method_name='get_discounted_price')


    def get_discounted_price(self, obj: Product):
        if obj.unit_price > 9:
            return obj.unit_price * Decimal(0.9)  # 10% discount
        return obj.unit_price
    

class ReviewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'ratings', 'name', 'description', 'created_at', 'rating_text']
    
    rating_text = serializers.SerializerMethodField(method_name="stars_text")

    def stars_text(self, obj: Review):
        return "⭐️" * obj.ratings
    
    def create(self, validated_data):
        product_id = self.context['product_id']
        validated_data['product_id'] = product_id
        return super().create(validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'unit_price']



class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'units', 'price']

    id = serializers.IntegerField(read_only=True)
    price = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    product = SimpleProductSerializer()
    
    def calculate_total_price(self, obj: CartItem):
        return obj.units * obj.product.unit_price




class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'items', 'total_price']
    
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')


    def calculate_total_price(self, obj: Cart):
        return sum([item.units * item.product.unit_price for item in obj.items.all()])
    

class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product_id', 'units']
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No product with the given ID was found.")
        return value

    def create(self, validated_data):
        cart_id = self.context['cart_pk']
        product_id = validated_data['product_id']
        units = validated_data['units']
        # print("Cart ID:", cart_id, "Product ID:", product_id, "Units:", units)
        try:
            cart_item = CartItem.objects.filter(cart_id=cart_id, product_id=product_id).get()
            # print("Existing Cart Item:", cart_item)
            units += cart_item.units
            price = 10 * units # static as we're are already calculating price when retrieving so this is useless
            CartItem.objects.filter(cart_id=cart_id, product_id=product_id).update(units=units, price=price)
            self.instance = cart_item
            self.instance.units = units
            self.instance.price = price
        except CartItem.DoesNotExist:
            price = 10 * units # static as we're are already calculating price when retrieving so this is useless
            self.instance = CartItem.objects.create(cart_id=cart_id, price=price, **validated_data)
        except Exception as e:
            print("Error:", e)
            raise e
        
        return self.instance
    
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['units']
        

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'units', 'price']
    product = ProductModelSerializer()

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','placed_at', 'payment_status', 'customer', 'items']
    items = OrderItemSerializer(many=True)
    customer = CustomerSerializer(read_only=True)


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, value):
        if not Cart.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No cart exists with the given id.")
        if CartItem.objects.filter(cart_id=value).count() == 0:
            raise serializers.ValidationError("cart is empty. please add one or more items to the cart before checking out.")
        return value

    @transaction.atomic
    def save(self, **kwargs):
        user_id = self.context['user_id']
        cart_id = self.validated_data['cart_id']
        print(user_id, cart_id)
        customer = Customer.objects.get(user_id=user_id)
        order = Order.objects.create(customer=customer)
        cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)
        order_items = [
            OrderItem(
                order=order,
                product = item.product,
                units = item.units,
                price = item.product.unit_price
            ) 
            for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)
        Cart.objects.filter(pk=cart_id).delete()

        order_created.send_robust(self.__class__, current_order=order)
        return order