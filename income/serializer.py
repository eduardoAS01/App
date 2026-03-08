from rest_framework import serializers
from .models import Income,SaleItem,Sale
from inventory.models import Product
from datetime import timezone
from .services import IncomeServices
from django.db import transaction

class SaleItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset = Product.objects.all(),write_only = True)
    
    class Meta():
        model = SaleItem
        fields = ("product","quantity")
 
    
    def validate(self,data):
        product = data["product"]
        quantity = data["quantity"]

        if quantity <= 0:
            raise serializers.ValidationError("Product quantity cant be zero")
        
        if quantity > product.quantity:
            raise serializers.ValidationError(f"Not enough stock for {product.name}")

        return data
        
            

class IncomeSerializer(serializers.ModelSerializer):
    
    products = SaleItemSerializer(many=True,required=False,write_only=True)
    
    class Meta():
        model = Income
        fields = ("income_type","comment","amount","products","created_at")
        read_only_fields = ('created_at',)
        extra_kwargs = {
            'amount':{'required':False}
        }
    
    
    def validate(self, data):
        income_type = data.get('income_type')
        products = data.get('products')
        amount = data.get('amount')
        product_ids = []
        
        if income_type == 'PRODUCT_SALE':
            if not products or len(products) == 0:
                raise serializers.ValidationError("Products: you must send at least one product")
            
            for item in products:
                product_id = item["product"].id

                if product_id in product_ids:
                    raise serializers.ValidationError("A product cannot appear twice in the same sale")
                
                product_ids.append(product_id)

            calculated_amount = IncomeServices.calculated_amount(products)
            
            if calculated_amount != amount and amount:
                raise serializers.ValidationError("Amount is not correct. Please check")
            
            
            data['amount'] = calculated_amount
        else:
            if amount is None or amount <= 0:
                raise serializers.ValidationError("Amount is needed for this income type")
    
            if products:
                raise serializers.ValidationError("This income type dont have products")
        
        return data
    
    def create(self, validated_data):
        
        return IncomeServices.create_income(validated_data) 


            
        
