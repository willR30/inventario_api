from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from api.models import Customer
from api.serializers import CustomerSerializer
from api.views import  get_business_id_by_user_from_server


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_customer(request):
    """
    Creates a new customer.

    JSON Input:
    {
      "first_name": "Customer First Name",
      "last_name": "Customer Last Name",
      "email": "customer@example.com",
      "phone": "123-456-7890",
      "c_address": "Customer Address",
      "business": 1  # Business ID
    }

    Returns:
    201 Created on success, 400 Bad Request on failure.
    """
    data = request.data
    serializer = CustomerSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Customer created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"error": "Failed to create the customer", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_customers(request):
    """
    Lists all customers associated with the authenticated user's business.

    Returns:
    200 OK with customer data on success.
    """
    business = get_business_id_by_user_from_server(request)
    customers = Customer.objects.filter(business_id=business)
    serializer = CustomerSerializer(customers, many=True)
    return Response({"message": "Customers listed successfully", "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_customer(request):
    """
    Updates an existing customer.

    JSON Input:
    {
      "customer_id": 1,  # Customer ID to update
      "first_name": "Updated Customer First Name",
      "last_name": "Updated Customer Last Name",
      "email": "updated_customer@example.com",
      "phone": "123-456-7890",
      "c_address": "Updated Customer Address"
    }

    Returns:
    200 OK with updated customer data on success, 400 Bad Request on failure, 404 Not Found if the customer doesn't exist.
    """
    data = request.data
    customer_id = data.get('customer_id')
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_customer(request):
    """
    Deletes a customer.

    JSON Input:
    {
      "customer_id": 1  # Customer ID to delete
    }

    Returns:
    204 No Content on success, 404 Not Found if the customer doesn't exist.
    """
    data = request.data
    customer_id = data.get('customer_id')
    try:
        customer = Customer.objects.get(pk=customer_id)
        customer.delete()
        return Response({"message": "Customer deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
