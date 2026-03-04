from inventory.models import Product
from rest_framework.exceptions import ValidationError
from .models import Income,Sale,SaleItem 


class IncomeServices():
    
    @staticmethod
    def calculated_amount(products:list):
        print(1)
        products_ids = [id['product'] for id in products]
        print(2)
        items = []
        amount = 0

        for item in products:
            product_id = item['product']
            quantity = item['quantity']
            
            total = product_id.sale_price * quantity
            amount += total
            items.append({
                "product":product_id,
                "quantity":quantity,
                "unit_price":product_id.sale_price,
                "total": total
            })
            

        return amount,items
    
    
    def create_sale_objects(self,validated_data:dict):
        user = validated_data.get('user')
        amount,items = self.calculated_amount(validated_data.get('products'))

        sale = Sale.objects.create(
            user = user,
            amount = amount
        )

        for item in items:
            SaleItem.objects.create(
                sale = sale,
                product = item['product'],
                quantity = item['quantity'],
                unit_price = item['unit_price'],
                total = item['total']
            )
        return sale
    



    