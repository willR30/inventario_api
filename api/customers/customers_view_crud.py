from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from sympy.logic.inference import valid

from api.models import Customer
from api.serializers import CustomerSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_customer(request):
    """
        Create a new customer in the database.

        This function expects to receive a JSON with the customer's data. The function validates the data and responds with a success message if the creation is successful.

        :param request: The HTTP request object.
        :return: Response with success message and data of the created customer.
    """
    data = request.data  # JSON with data for the new customer
    serializer = CustomerSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Customer created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"error": "Failed to create the customer", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def list_customers(request):
    """
        List all customers associated with a specific business.

        This function expects to receive the business's ID as part of the JSON.

        :param request: The HTTP request object.
        :return: Response with success message and a list of customers associated with the business.
    """
    business_id = request.data.get('business_id')  # Business ID
    customers = Customer.objects.filter(business__id=business_id)
    serializer = CustomerSerializer(customers, many=True)
    return Response({"message": "Customers listed successfully", "data": serializer.data}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_customer(request):
    """
    Update the information of an existing customer in the database.

    This function expects to receive a JSON with the updated customer data, including the ID of the customer to be updated.

    :param request: The HTTP request object.
    :return: Response with success message and the data of the updated customer.
    
    """
    data = request.data  # JSON with updated customer data
    customer_id = data.get('customer_id')  # Get the customer ID from the JSON
    try:
        customer = Customer.objects.get(pk=customer_id)
        serializer = CustomerSerializer(customer, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Customer updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"error": "Failed to update the customer", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_customer(request):
    """
    Delete a customer from the database.

    This function expects to receive the ID of the customer to be deleted as part of the JSON.

    :param request: The HTTP request object.
    :return: Response with a success message confirming the deletion.
    """
    data = request.data  # JSON with the customer ID to delete
    customer_id = data.get('customer_id')  # Get the customer ID from the JSON
    try:
        customer = Customer.objects.get(pk=customer_id)
        customer.delete()
        return Response({"message": "Customer deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
