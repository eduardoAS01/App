from django.db import models
from inventory.models import Product

# Create your models here.

class StockMovement(models.Model):

    class Reason(models.TextChoices):
        PURCHASE = "PURCHASE"
        SALE = "SALE"
        ADJUSTMENT = "ADJUSTMENT"
        RETURN = "RETURN"

    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="Product id")
    old_quantity = models.IntegerField(verbose_name="product quantity before",default=0)
    new_quantity = models.IntegerField(verbose_name="Product quantity after",default=0)
    reason = models.CharField(max_length=20,choices=Reason.choices,verbose_name="Stock movement reason")
    comment = models.CharField(max_length=250,blank=True,verbose_name="Comment")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Change date") 

    def __str__(self):
        return f"Product id: {self.product_id} - quantity: {self.quantity} - reason: {self.reason}"