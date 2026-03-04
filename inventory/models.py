from django.db import models
from decimal import Decimal
from django.conf import settings

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=80,verbose_name="Product name",unique=True)
    description = models.CharField(max_length=250,verbose_name="Product description",blank=True)
    quantity = models.IntegerField(default=0,verbose_name="Product quantity")
    cost_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Product cost price")
    sale_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Product sale price")
    active = models.BooleanField(default=True,verbose_name="Product still saling")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Preoduct created date")

    def __str__(self):
        return self.name
    
    @property
    def profit(self):
        return self.sale_price - self.cost_price
    
    @property
    def profit_percentage(self):
        if self.cost_price == 0:
            return Decimal("0")
        return round((self.profit/self.cost_price) * 100)

"""
class StockMovement(models.Model):

    class Reason(models.TextChoices):
        PURCHASE = "PURCHASE"
        SALE = "SALE"
        ADJUSTMENT = "ADJUSTMENT"
        RETURN = "RETURN"

    product_id = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="Product id")
    quantity = models.IntegerField(verbose_name="Product quantity")
    reason = models.CharField(max_length=20,choices=Reason.choices,verbose_name="Stock movement reason")
    comment = models.CharField(max_length=250,verbose_name="Comment")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Change date") 

    def __str__(self):
        return f"Product id: {self.product_id} - quantity: {self.quantity} - reason: {self.reason}"
"""
