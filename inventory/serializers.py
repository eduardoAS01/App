from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    profit = serializers.ReadOnlyField()
    profit_percentage = serializers.ReadOnlyField()
    

    class Meta():
        model = Product
        fields = ("id","name","description","cost_price","sale_price","active","created_at","profit","profit_percentage","quantity")
        read_only_fields = ("created_at",)

    def validate(self, data):

        cost = data.get("cost_price")
        sale = data.get("sale_price")
        quantity = data.get("quantity")
        
        if cost is not None and cost <= 0:
            raise serializers.ValidationError({"cost_price":"Cost price must be greater than zero."})

        if sale is not None and sale <= 0:
            raise serializers.ValidationError({"sale_price":"Sale price must be greater than zero."})

        if quantity is not None and quantity <= 0:
            raise serializers.ValidationError({"quantity":"Product quantity must be greater than zero."})
    
        return data
    
    def vaidate_name(self,value):
        if Product.objects.filter(name__iexact = value).exists():
            raise serializers.ValidationError("A product with this name already exists.")
        return value
    