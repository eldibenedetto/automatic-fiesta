from rest_framework import serializers

from .models import (Customer, Subscription, Gift)

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