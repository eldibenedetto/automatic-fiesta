from django.test import TestCase
from django.utils import timezone
import json
from django.db.utils import IntegrityError
from .models import Customer, Subscription, Gift
from django.urls import reverse
# from .views import CustomerViewSet

class CustomerTest(TestCase):

    def create_customer(self,
        id="b73b8b0e-5678-42a9-874c-00445d51dd8a",
        first_name="Ludwig", last_name="Beethoven",
        address_1="574 Austrian Ave.",
        address_2="Apt 9",
        city="Brooklyn",
        state="NY",
        postal_code="11217"):
        return Customer.objects.create(id=id, first_name=first_name, last_name=last_name, address_1=address_1, address_2=address_2, city=city, state=state, postal_code=postal_code)

    def test_customer_creation(self):
        c = self.create_customer()
        # Check Customer is created correctly
        self.assertTrue(isinstance(c, type(Customer())))
        self.assertTrue(c.id == "b73b8b0e-5678-42a9-874c-00445d51dd8a")

class SubscriptionTest(TestCase):

    def create_subscription(self, id="eac8709f-e898-42f0-84d8-a1997c25cae9", plan_name="print & digital", price="5999", customer_id=None):
        return Subscription.objects.create(id=id, plan_name=plan_name, price=price, customer_id=customer_id)

    def test_subscription_creation(self):
        c = CustomerTest.create_customer(self)
        s = self.create_subscription(customer_id=c)
        # Check Subscription is created correctly
        self.assertTrue(isinstance(s, type(Subscription())))
        self.assertTrue(s.customer_id.id == c.id)
        # Check ownership
        with self.assertRaises(Exception) as raised:
            self.create_subscription()
        self.assertEqual(IntegrityError, type(raised.exception), msg='Subscription must belong to a Customer')

class GiftTest(TestCase):

    def create_gift(self, id="eac8709f-e898-42f0-84d8-a1997c25cae9", plan_name="print & digital", price="5999", recipient_email="amadeus@mozart.com", customer_id=None):
        return Gift.objects.create(id=id, plan_name=plan_name, price=price, recipient_email=recipient_email, customer_id=customer_id)

    def test_gift_creation(self):
        c = CustomerTest.create_customer(self)
        g = self.create_gift(customer_id=c)
        # Check Gift is created correctly
        self.assertTrue(isinstance(g, type(Gift())))
        # Check Customer.id
        self.assertTrue(g.customer_id.id == c.id)
        # Check Customer owns Gift
        with self.assertRaises(Exception) as raised:
            self.create_gift()
        self.assertEqual(IntegrityError, type(raised.exception), msg='Gift must belong to a Customer')
