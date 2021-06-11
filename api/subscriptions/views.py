from rest_framework.views import APIView
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.response import Response
from rest_framework import status
from pprint import pprint

class CustomerList(APIView):
	"""
	List all customers, or create a new customer.
	"""
	def get(self, request, format=None):
		customers = Customer.objects.all()
		serializer = CustomerSerializer(customers, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		data = request.data['customer']
		serializer = CustomerSerializer(data=data)
		print(serializer.is_valid())
		if serializer.is_valid():
			serializer.save()
			print(serializer.data)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

