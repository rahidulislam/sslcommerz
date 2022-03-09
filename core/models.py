from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BillingAddess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="billing_user")
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    country = models.CharField(max_length=50)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_user")
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    tran_id = models.CharField(max_length=50, blank=True)
    cus_name = models.CharField(max_length=50)
    cus_email = models.EmailField(max_length=254)
    cus_phone = models.CharField(max_length=50)
    num_of_item = models.IntegerField(default=1)
    product_name = models.CharField(max_length=50)
    product_category = models.CharField(max_length=50)

    def __str__(self):
        return self.cus_name

