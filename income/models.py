from django.db import models
from django.conf import settings
from inventory.models import Product
from business.models import Business


class Sale(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name="User",db_index=True)
    date = models.DateTimeField(auto_now_add=True,verbose_name="Sale date",db_index=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Sale amount")
    business = models.ForeignKey(Business,on_delete=models.CASCADE,db_index=True)

    def __str__(self):
        return f"{self.user} Amount: {self.amount}" 
    
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale,on_delete=models.CASCADE,verbose_name="Sale id",related_name="products")
    business = models.ForeignKey(Business,on_delete=models.CASCADE,db_index=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="Product id",db_index=True)
    quantity = models.IntegerField(verbose_name="Quantity")
    unit_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Product individual sale price")
    total = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Total")

    def __str__(self):
        return f"{self.product}"
    
class Income(models.Model):

    class IncomeType(models.TextChoices):
        PRODUCT_SALE = "PRODUCT_SALE"
        LOAN = "LOAN"
        ASSET_SALE = "ASSET_SALE"
        INTEREST = "INTEREST"
        OTHER = "OTHER"

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name="User",db_index=True)
    business = models.ForeignKey(Business,on_delete=models.CASCADE,db_index=True)
    sale = models.OneToOneField(Sale,on_delete=models.CASCADE,null=True,blank=True)
    income_type = models.CharField(max_length=20,choices=IncomeType.choices)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    comment = models.CharField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)

    