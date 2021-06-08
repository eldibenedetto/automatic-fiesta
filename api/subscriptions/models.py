from django.db import models

# Create your models here.
from django.db import models

# Assumptions:
#  1) In order to be a customer you must have some kind of subscription
#  2) A gift belongs to a customer

class Customer(models.Model):
    id = models.CharField(primary_key=True, max_length=100, blank=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    address_1 = models.CharField(max_length=50)
    address_2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=5)
    postal_code = models.CharField(max_length=10)

class Subscription(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    customer_id = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='subscription', null=False)
    plan_name = models.CharField(max_length=20)
    price = models.CharField(max_length=10)

class Gift(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='gifts', null=False)
    plan_name = models.CharField(max_length=20)
    price = models.CharField(max_length=10)
    recipient_email = models.CharField(max_length=20)