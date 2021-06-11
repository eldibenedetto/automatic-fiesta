import json
from pprint import pprint
from .models import (Customer, Subscription, Gift)
from .serializers import CustomerSerializer
import sys
import os


def create_customer(customer_data):
    try:
        return Customer.objects.create(**customer_data)
    except:
        raise ValueError('Customer Already Created.')

def create_gifts(gifts_list, custy):
    try:
        gift_objs = list(map(lambda x: Gift(customer=custy, **x), gifts_list))
        return Gift.objects.bulk_create(gift_objs)
    except:
        raise ValueError('Gift Already Created.')

def create_subscription(sub_data, custy):
    try:
        return Subscription.objects.create(customer=custy, **sub_data)
    except:
        raise ValueError('Subscription Already Created.')

def create_instances(instance_data):
    customer_data = instance_data['customer_data']
    customer = create_customer(customer_data)
    subscription_data = instance_data['subscription_data']
    if subscription_data is not None:
        sub = create_subscription(subscription_data, customer)
    else:
        raise ValueError('Subscription information is blank. A Customer must have a subscription.')
    gifts_data = instance_data['gifts_data']
    gifts = create_gifts(gifts_data, customer)
    return {
        "customer": customer,
        "subscription": sub,
        "gifts": gifts
    }

def parse_payload(body):
    request_body = json.loads(body)
    try:
        customer_data = request_body['customer']
        subscription_data = request_body['customer'].pop('subscription')
        gifts_data = request_body['customer'].pop('gifts')
        return {
            "customer_data": customer_data,
            "subscription_data": subscription_data,
            "gifts_data": gifts_data,
        }
    except Exception as e:
        key_name = str(e).replace('KeyError: ', '')
        raise ValueError(f'Key: {key_name} is required.')