
from decimal import Decimal
from django.db.models import Sum
from .models import Cart, CartItem, Product, Collection, Review
from rest_framework import serializers


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
        try:
            cart_item = CartItem.objects.filter(cart_id=cart_id, product_id=product_id).get()
            units += cart_item.units
            price = 10 * units # static as we're are already calculating price when retrieving so this is useless
            self.instance = CartItem.objects.filter(cart_id=cart_id, product_id=product_id).update(units=units, price=price)
        except CartItem.DoesNotExist:
            price = 10 * units # static as we're are already calculating price when retrieving so this is useless
            self.instance = CartItem.objects.create(cart_id=cart_id, price=price, **validated_data)
        
        return self.instance
    
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['units']
        