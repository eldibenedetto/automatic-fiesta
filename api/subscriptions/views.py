from rest_framework.viewsets import (ModelViewSet, GenericViewSet)
import json
from .models import (Customer, Subscription, Gift)
from .serializers import CustomerSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins

# Create your views here.
class CustomerViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        GenericViewSet):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer

	def create_gifts(self, gifts_list, custy):
		return list(map(lambda x: Gift.objects.create(customer_id=custy, **x), gifts_list))
	
	def create_subscription(self, sub_data, custy):
		return Subscription.objects.create(customer_id=custy, **sub_data)

	def create_instances(self, instance_data):
		customer_data = instance_data['customer_data']
		customer = Customer.objects.create(**customer_data)
		subscription_data = instance_data['subscription_data']
		if subscription_data is not None:
			sub = self.create_subscription(subscription_data, customer)
		else:
			raise ValueError('Subscription information is blank. A Customer must have a subscription.')
		gifts_data = instance_data['gifts_data']
		gifts = self.create_gifts(gifts_data, customer)
		return {
			"customer": customer,
			"subscription": sub,
			"gifts": gifts
		}

	def build_response(self, custy=None, msg=None):
		if custy is not None:
			serializer = self.get_serializer(custy)
			headers = self.get_success_headers(serializer.data)
			return {
				"data": serializer.data,
				"headers": headers,
				"status": status.HTTP_201_CREATED
			}
		else:
			return {
				"data": {'error': msg},
				"status": status.HTTP_400_BAD_REQUEST
			}
	
	def parse_payload(self, body):
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

	def create(self, request, *args, **kwargs):
		try:
			# Parse/Validate Payload
			instance_data = self.parse_payload(request.body)
			# Create Function
			instances = self.create_instances(instance_data)
			# Build Response
			response = self.build_response(instances['customer'])
			return Response(response['data'], status=response['status'], headers=response['headers'])
		except Exception as e:
			response = self.build_response(msg=str(e))
			return Response(response['data'], status=response['status'])