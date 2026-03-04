from rest_framework import serializers
from .models import Income,SaleItem,Sale
from inventory.models import Product
from datetime import timezone
from .services import IncomeServices


class SaleItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset = Product.objects.all(),write_only = True)

    class Meta():
        model = SaleItem
        fields = ("product","quantity")

    def validate_product_id(self, value):
        if not Product.objects.filter(id = value).exists():
            raise serializers.ValidationError(f"Product with this ID: {value} dont exists")
        return value
    
    def validate_quantity(self,value):
        if value <= 0:
            raise serializers.ValidationError("Product quantity cant be zero")
        return value
        
            

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
        
        if income_type == 'PRODUCT_SALE':
            if not products or len(products) == 0:
                raise serializers.ValidationError("Products: you must send at least one product")
            
            calculated_amount, _ = IncomeServices.calculated_amount(products)
            
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
        
        if validated_data["income_type"] == "PRODUCT_SALE":
            income_service = IncomeServices()
            sale = income_service.create_sale_objects(validated_data)
        else:
            sale = None
            
        income = Income.objects.create(
            user = validated_data['user'],
            sale = sale,
            income_type = validated_data['income_type'],
            amount = validated_data['amount'],
            comment = validated_data.get('comment')
        )
        
        return income

class SaleItemShow(serializers.ModelSerializer):
    class Meta():
        model  = SaleItem
        fields = ("sale","product","quantity","unit_price","total")
        
        
            
        
