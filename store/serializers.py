
from decimal import Decimal
from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True)
    price = serializers.DecimalField(max_digits=5, decimal_places=2, source='unit_price')
    discount_price = serializers.SerializerMethodField(method_name="calculate_discounted_price")

    def calculate_discounted_price(self, obj):
        if obj.unit_price > 9:
            return obj.unit_price * Decimal(0.9)  # 10% discount
        return obj.unit_price