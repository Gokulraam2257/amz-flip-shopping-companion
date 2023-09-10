from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recent_item_purchase = models.CharField(max_length=255, blank=True, null=True)
    total_purchases = models.PositiveIntegerField(default=0)
    monthly_expenses = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    purchase_limit = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    favorite_category = models.CharField(max_length=255, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=15,null=True)

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prod_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    date_time = models.DateTimeField(auto_now_add=True)
    SOURCE_CHOICES = [
        ('amz', 'Amazon'),
        ('flip', 'Flipkart')
    ]
    source = models.CharField(max_length=4, choices=SOURCE_CHOICES)



class PriceAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prod_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    old_price = models.DecimalField(max_digits=8, decimal_places=2)
    drop = models.DecimalField(max_digits=5, decimal_places=2)
