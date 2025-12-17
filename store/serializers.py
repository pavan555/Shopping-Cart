
from decimal import Decimal
from .models import Product, Collection, Review
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
    