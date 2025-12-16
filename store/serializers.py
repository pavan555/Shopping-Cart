
from decimal import Decimal
from .models import Product, Collection
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
        view_name='collection-details'
    )

    def calculate_discounted_price(self, obj: Product):
        if obj.unit_price > 9:
            return obj.unit_price * Decimal(0.9)  # 10% discount
        return obj.unit_price


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'unit_price', 'discounted_price', 'collection']
    
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-details'
    # )

    discounted_price = serializers.SerializerMethodField(method_name='get_discounted_price')


    def get_discounted_price(self, obj: Product):
        if obj.unit_price > 9:
            return obj.unit_price * Decimal(0.9)  # 10% discount
        return obj.unit_price