from django.db import models
from inventory.models import Product
from expense.models import Purchase
from income.models import Sale
from business.models import Business

class StockMovement(models.Model):

    class Reason(models.TextChoices):
        INITIAL = "INITIAL"
        PURCHASE = "PURCHASE"
        SALE = "SALE"
        ADJUSTMENT = "ADJUSTMENT"
        RETURN = "RETURN"

    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="Product id",db_index=True)
    business = models.ForeignKey(Business,on_delete=models.CASCADE,db_index=True)
    old_quantity = models.IntegerField(verbose_name="product quantity before",default=0)
    new_quantity = models.IntegerField(verbose_name="Product quantity after",default=0)
    quantity_change = models.IntegerField(verbose_name="quantity difference",default=0)
    sale = models.ForeignKey(Sale,on_delete=models.CASCADE,null=True)
    purchase = models.ForeignKey(Purchase,on_delete=models.CASCADE,null=True)
    reason = models.CharField(max_length=20,choices=Reason.choices,verbose_name="Stock movement reason")
    comment = models.CharField(max_length=250,blank=True,verbose_name="Comment")
    
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Change date",db_index=True) 

    def __str__(self):
        return f"Product id: {self.product} - quantity: {self.new_quantity} - reason: {self.reason}"