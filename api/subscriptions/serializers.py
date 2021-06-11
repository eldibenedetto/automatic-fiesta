from rest_framework import serializers
from pprint import pprint
from collections import OrderedDict
from .models import (Customer, Subscription, Gift)
import sys
import os

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'plan_name', 'price']

class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        fields = ['id', 'plan_name', 'price', 'recipient_email']


class CustomerSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer(many=False)
    gifts = GiftSerializer(many=True)
    class Meta:
        model = Customer
        fields = ('id', 'first_name', 'last_name', 'address_1', 'address_2', 'city', 'state', 'postal_code', 'subscription', 'gifts')

    def create(self, validated_data):
        sub_data = dict(OrderedDict(validated_data.pop('subscription')))
        gifts_data = validated_data.pop('gifts')
        gifts = list(map(lambda x: dict(OrderedDict(x)), gifts_data))
        customer = Customer.objects.create(**validated_data)
        Subscription.objects.create(**sub_data, customer=customer)
        for gift in gifts:
            Gift.objects.create(customer=customer, **gift)
        return customer