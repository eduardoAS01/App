from inventory.models import Product
from rest_framework.exceptions import ValidationError
from .models import Purchase,PurchaseItem,Expense
from invetory_record.models import StockMovement
from django.db import transaction
from django.db.models import F


class ExpenseServices():
    
    @staticmethod
    def calculated_amount(products:list):
        amount = 0

        for item in products:
            product = item["product"]
            quantity = item["quantity"]
            
            total = product.cost_price * quantity
            amount += total
            
        return amount
    
    @staticmethod
    def create_expense(validated_data:dict):
        
        with transaction.atomic():
        
            user = validated_data.get('user')
            products = validated_data.pop("products",[])
            expense_type = validated_data["expense_type"]
            
            purchase = None
            amount = validated_data['amount']
            

            
            if expense_type == "PRODUCT_PURCHASE":
                
                purchase = Purchase.objects.create(
                    user = user,
                    amount = amount
                )
                
                for item in products:
                    try:
                        product = Product.objects.select_for_update().get(id=item["product"].id,user=user)
                    except Product.DoesNotExist:
                        raise ValidationError("product not found")
                    
                    quantity = item["quantity"]
                    
                    unit_price = product.cost_price

                    
                    total = unit_price * quantity
                    
                    PurchaseItem.objects.create(
                        purchase = purchase,
                        product = product,
                        quantity = quantity,
                        unit_price = unit_price,
                        total = total
                    )
                    
                    old_quantity = product.quantity
                    product.quantity = F("quantity") + quantity
                    change = product.quantity - old_quantity
                    product.save()
                    product.refresh_from_db()
                    
                    StockMovement.objects.create(
                        product = product,
                        new_quantity = quantity,
                        old_quantity = old_quantity,
                        quantity_change = change,
                        purchase = purchase,
                        reason = "PURCHASE"
                    )
                                        
            
            expense = Expense.objects.create(
                user = user,
                purchase = purchase,
                expense_type = expense_type,
                amount = amount,
                comment = validated_data.get('comment',"")
            )
            
            return expense