from inventory.models import Product
from rest_framework.exceptions import ValidationError
from .models import Income,Sale,SaleItem 
from invetory_record.models import StockMovement
from django.db import transaction
from django.db.models import F


class IncomeServices():
    
    @staticmethod
    def calculated_amount(products:list):
        amount = 0

        for item in products:
            product = item["product"]
            quantity = item["quantity"]
            
            total = product.sale_price * quantity
            amount += total
            
        return amount
    
    @staticmethod
    def create_income(validated_data:dict):
        
        with transaction.atomic():
        
            user = validated_data.get('user')
            business = validated_data.get('business')
            products = validated_data.pop("products",[])
            income_type = validated_data["income_type"]
            
            sale = None
            amount = validated_data['amount']
            

            
            if income_type == "PRODUCT_SALE":
                
                sale = Sale.objects.create(
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
                    
                    if quantity > product.quantity:
                        raise ValidationError("Not enough stock")
                    
                    unit_price = product.sale_price

                    
                    total = unit_price * quantity
                    
                    SaleItem.objects.create(
                        sale = sale,
                        product = product,
                        quantity = quantity,
                        unit_price = unit_price,
                        total = total,
                        business = business
                    )
                    
                    old_quantity = product.quantity
                    product.quantity = F("quantity") - quantity
                    product.save()
                    product.refresh_from_db()
                    change = product.quantity - old_quantity
                    new_quantity = old_quantity + change
                    
                    StockMovement.objects.create(
                        product = product,
                        new_quantity = new_quantity,
                        old_quantity = old_quantity,
                        quantity_change = change,
                        sale = sale,
                        reason = "SALE",
                        business = business
                    )
                                        
            
            income = Income.objects.create(
                user = user,
                sale = sale,
                income_type = income_type,
                amount = amount,
                business = business,
                comment = validated_data.get('comment',"")
            )
            
            return income
    



    