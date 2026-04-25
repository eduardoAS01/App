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
            business = validated_data.get("business")
            
            purchase = None
            amount = validated_data['amount']
            

            
            if expense_type == "PURCHASE_PRODUCT":
                
                purchase = Purchase.objects.create(
                    user = user,
                    amount = amount,
                    business = business
                )
                
                for item in products:
                    try:
                        product = Product.objects.select_for_update().get(id=item["product"].id,business=business)
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
                        total = total,
                        business = business
                    )
                    
                    old_quantity = product.quantity
                    product.quantity = F("quantity") + quantity
                    product.save()
                    product.refresh_from_db()
                    change = product.quantity - old_quantity
                    new_quantity = old_quantity + change
                    
                    StockMovement.objects.create(
                        product = product,
                        new_quantity = new_quantity,
                        old_quantity = old_quantity,
                        quantity_change = change,
                        purchase = purchase,
                        reason = "PURCHASE",
                        business = business
                    )
                                        
            
            expense = Expense.objects.create(
                user = user,
                purchase = purchase,
                expense_type = expense_type,
                amount = amount,
                comment = validated_data.get('comment',""),
                business = business
            )
            
            return expense