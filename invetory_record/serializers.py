from rest_framework import serializers
from .models import StockMovement

class StockMovementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source ="product.name",read_only = True)

    class Meta():
        model = StockMovement
        fields = ("product","product_name","old_quantity","new_quantiy","quantity_change","reason","comment","created_at")