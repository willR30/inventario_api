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
            Create a new product.

            This function expects a JSON with product data to create a new product. If the product is created successfully,
            it responds with a success message and the product data. If there are validation errors in the data, it returns an error
            message with details.

            :param request: The HTTP request object.
            :return: Response with a success message and product data if the product is created, or an error message if creation fails.

            Example JSON Request:
            {
                "photo_link": "product_photo_url",
                "name": "Product Name",
                "description": "Product description",
                "stock": 10,
                "cost_price": 7.5,
                "sale_price": 10.0,
                "category_id": 1,
                "business_id": 1,
                "with_iva": true
            }

            Example JSON Response:
            {
                "message": "Product created successfully",
                "data": {
                    "id": 1,
                    "name": "Product Name",
                    "description": "Product description",
                    "stock": 10,
                    "cost_price": 7.5,
                    "sale_price": 10.0,
                    "category_id": 1,
                    "business_id": 1,
                    "with_iva": true
                }
            }

            Status Codes:
            - 201 Created: If the product is created successfully.
            - 400 Bad Request: If there are validation errors or other issues.
    """
    data = request.data  # JSON with data for the new customer
    serializer = CustomerSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Customer created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"error": "Failed to create the customer", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_customers(request):
    business = get_business_id_by_user_from_server(request)
    customers = Customer.objects.filter(business_id=business)
    serializer = CustomerSerializer(customers, many=True)
    return Response({"message": "Customers listed successfully", "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_customer(request):
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_customer(request):
    data = request.data  # JSON with the customer ID to delete
    customer_id = data.get('customer_id')  # Get the customer ID from the JSON
    try:
        customer = Customer.objects.get(pk=customer_id)
        customer.delete()
        return Response({"message": "Customer deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
