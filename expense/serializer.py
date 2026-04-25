from rest_framework import serializers
from .models import Expense,PurchaseItem,Purchase
from inventory.models import Product
from .services import ExpenseServices


class PurchaseItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset = Product.objects.all())
    product_name = serializers.CharField(source ="product.name",read_only = True)

    class Meta():
        model = PurchaseItem
        fields = ("product","product_name","quantity","unit_price","total")
        read_only_fields = ("unit_price","total")

    def validate(self,data):
        quantity = data["quantity"]

        if quantity <= 0:
            raise serializers.ValidationError("Product quantity cant be zero")
        
        return data
    
class PurchaseSerializer(serializers.ModelSerializer):
    products = PurchaseItemSerializer(many = True,read_only=True)

    class Meta():
        model = Purchase
        fields = ("amount","date","products")

class ExpenseSerializer(serializers.ModelSerializer):
    
    products = PurchaseItemSerializer(many = True,required = False,write_only=True)

    class Meta():
        model = Expense
        fields = ("expense_type","comment","amount","products","created_at")
        read_only_fields = ("created_at",)
        extra_kwargs = {
            'amount':{'required':False}
        }

    def validate(self, data):
        expense_type = data.get('expense_type')
        products = data.get('products')
        amount = data.get('amount')
        product_ids = []
        
        if expense_type == 'PURCHASE_PRODUCT':
            if not products or len(products) == 0:
                raise serializers.ValidationError("Products: you must send at least one product")
            
            for item in products:
                product_id = item["product"].id

                if product_id in product_ids:
                    raise serializers.ValidationError("A product cannot appear twice in the same purchase")
                
                product_ids.append(product_id)

            calculated_amount = ExpenseServices.calculated_amount(products)
            
            if calculated_amount != amount and amount:
                raise serializers.ValidationError(f"The correct amount is: {calculated_amount}")
            
            
            data['amount'] = calculated_amount
        else:
            if amount is None or amount <= 0:
                raise serializers.ValidationError("Amount is needed for this purchase type")
    
            if products:
                raise serializers.ValidationError("This purchase type dont have products")
        
        return data
    
    def create(self, validated_data):
        return ExpenseServices.create_expense(validated_data)
        
