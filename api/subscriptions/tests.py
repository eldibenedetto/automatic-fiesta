from django.test import TestCase
from django.utils import timezone
import json
from django.db.utils import IntegrityError
from .models import Customer, Subscription, Gift
from django.urls import reverse
from .views import CustomerViewSet

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

json_list_2 = [
    {
        "id": "53368db4-6097-49c6-ba8b-b00ab4a3ce3b",
        "plan_name": "digital",
        "price": "4999",
        "recipient_email": "mark@twain.com"
    },
    {
        "id": "fb7a077b-928f-4d44-a2e5-6969c72d3b45",
        "plan_name": "digital",
        "price": "4999",
        "recipient_email": "jane@austin.com"
    }
]
json_list_1 = [
    {
        "id": "fc7a077b-928f-4d44-a2e5-6969c72d3b45",
        "plan_name": "digital",
        "price": "4999",
        "recipient_email": "jane@austin.com"
    }
]
json_list_0 = []

sub_data = {
    "id": "eac8709f-d898-42f0-84d8-a1997c25cae9",
    "plan_name": "print & digital",
    "price": "5999"
}

full_json = {
    "customer": {
        "id": "b73b8b0e-0240-42a9-874c-00445d51dd8a",
        "first_name": "Ernest",
        "last_name": "Hemingway",
        "address_1": "907 Whitehead St",
        "address_2": "",
        "city": "Key West",
        "state": "FL",
        "postal_code": "33043",
        "subscription": {
            "id": "eac8709f-d898-42f0-84d8-a1997c25cae9",
            "plan_name": "print & digital",
            "price": "5999",
        },    
        "gifts":[
            {
                "id": "53368db4-6097-49c6-ba8b-b00ab4a3ce3b",
                "plan_name": "digital",
                "price": "4999",
                "recipient_email": "mark@twain.com"
            },
            {
                "id": "fb7a077b-928f-4d44-a2e5-6969c72d3b45",
                "plan_name": "digital",
                "price": "4999",
                "recipient_email": "jane@austin.com"
            }
        ]
    }
}
no_sub_json = {
    "customer": {
        "id": "c73b8b0e-0240-42a9-874c-00445d51dd8a",
        "first_name": "Ernest",
        "last_name": "Hemingway",
        "address_1": "907 Whitehead St",
        "address_2": "",
        "city": "Key West",
        "state": "FL",
        "postal_code": "33043",   
        "gifts":[
            {
                "id": "63368db4-6097-49c6-ba8b-b00ab4a3ce3b",
                "plan_name": "digital",
                "price": "4999",
                "recipient_email": "mark@twain.com"
            },
            {
                "id": "gb7a077b-928f-4d44-a2e5-6969c72d3b45",
                "plan_name": "digital",
                "price": "4999",
                "recipient_email": "jane@austin.com"
            }
        ]
    }
}
no_gifts_json = {
    "customer": {
        "id": "d73b8b0e-0240-42a9-874c-00445d51dd8a",
        "first_name": "Ernest",
        "last_name": "Hemingway",
        "address_1": "907 Whitehead St",
        "address_2": "",
        "city": "Key West",
        "state": "FL",
        "postal_code": "33043",
        "subscription": {
            "id": "fac8709f-d898-42f0-84d8-a1997c25cae9",
            "plan_name": "print & digital",
            "price": "5999",
        },    
        "gifts":[]
    }
}

class CustomerViewSetTest(TestCase):

    def test_customer_list_view(self):
        c = CustomerTest.create_customer(self)
        url = reverse('customer-list')
        resp = self.client.get(url)
        # Check Status Code
        self.assertEqual(resp.status_code, 200)
        # Check instance is returned in response
        self.assertIn(c.id, resp.json()[0]['id'])
    
    def test_gifts_create_view(self):
        json_lists =[json_list_2, json_list_1, json_list_0]
        c = CustomerTest.create_customer(self)
        # Check right number of Gifts created
        for json_list in json_lists:
            gifts = CustomerViewSet.create_gifts(CustomerViewSet, json_list, c)
            res = all(isinstance(sub, type(Gift())) for sub in gifts)
            self.assertTrue(res)
            self.assertTrue(len(json_list) == len(gifts))
    
    def test_subscription_create_view(self):
        c = CustomerTest.create_customer(self)
        sub = CustomerViewSet.create_subscription(CustomerViewSet, sub_data, c)
        self.assertTrue(isinstance(sub, type(Subscription())))
    
    def test_parse_payload_view(self):
        with self.assertRaises(Exception) as raised:
            CustomerViewSet.parse_payload(CustomerViewSet, json.dumps(no_sub_json))
        self.assertEqual(ValueError, type(raised.exception), msg="Key: 'subscription' is required.")

    def test_create_instances_view(self):
        poss_request_data = [full_json, no_sub_json, no_gifts_json]
        for req_data in poss_request_data:
            url = reverse('customer-list')
            resp = self.client.post(url, req_data)
            # Check Status Code
            if 'subscriptions' in req_data:
                self.assertEqual(resp.status_code, 200)
            else:
                self.assertEqual(resp.status_code, 400)