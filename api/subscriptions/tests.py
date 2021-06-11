from django.test import TestCase
from django.utils import timezone
import json
from collections import OrderedDict
from django.db.utils import IntegrityError
from .models import Customer, Subscription, Gift
from django.urls import reverse
from .serializers import CustomerSerializer

class CustomerSerializerCreateTest(TestCase):

    def test_serializer(self):
        Customer(id="b73b8b0e-5678-42a9-874c-00445d51dd8a",
            first_name="Ludwig", last_name="Beethoven",
            address_1="574 Austrian Ave.",
            address_2="Apt 9",
            city="Brooklyn",
            state="NY",
            postal_code="11217")
        


