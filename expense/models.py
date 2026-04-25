from django.db import models
from django.conf import settings
from inventory.models import Product
from business.models import Business


class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,db_index=True)
    date = models.DateTimeField(auto_now_add=True,verbose_name="Purchase date",db_index=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Purchase amount")
    supplier = models.CharField(max_length=100,blank=True,verbose_name="Supplier")
    business = models.ForeignKey(Business,on_delete=models.CASCADE,db_index=True)

    def __str__(self):
        return f"{self.user} Amount: {self.amount}"
    
class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase,on_delete=models.CASCADE,verbose_name="Purchase id",related_name="products")
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="Product id",db_index=True)
    quantity = models.IntegerField(verbose_name="quantity")
    unit_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Price per unit")
    total = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Purchase total")
    business = models.ForeignKey(Business,on_delete=models.CASCADE,db_index=True)

    def __str__(self):
        return f"{self.product}"

class Expense(models.Model):

    class ExpenseType(models.TextChoices):
        PURCHASE_PRODUCT = "PURCHASE_PRODUCT"
        PAYMENTS = "PAYMENTS"
        PURCHASE_ASSET = "PURCHASE ASSET"
        RENT = "RENT"
        SERVICES = "SERVICES"
        OTHER = "OTHER"

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,db_index=True)
    business = models.ForeignKey(Business,on_delete=models.CASCADE,db_index=True)
    purchase = models.OneToOneField(Purchase,on_delete=models.CASCADE,null=True)
    expense_type = models.CharField(max_length=30,choices=ExpenseType.choices)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    comment = models.CharField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
