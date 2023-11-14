from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from api.models import Supplier
from api.serializers import SupplierSerializer
from api.views import get_business_id_by_user_from_server
from rest_framework.authentication import TokenAuthentication


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_supplier(request):
    """
    Creates a new supplier record.

    JSON Input:
    {
      "name": "Supplier Name",
      "email": "supplier@email.com",
      "phone": "1234567890",
      "address": "Supplier Address"
    }

    Returns:
    201 Created with success message and created supplier data on success,
    400 Bad Request with error details if the input is invalid.
    """
    data = request.data  # JSON with data for the new supplier
    serializer = SupplierSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Supplier created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"error": "Failed to create the supplier", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_suppliers(request):
    """
    Lists suppliers associated with the authenticated user's business.

    Returns:
    200 OK with supplier data on success.
    """
    business = get_business_id_by_user_from_server(request)
    suppliers = Supplier.objects.filter(business_id=business)
    serializer = SupplierSerializer(suppliers, many=True)
    return Response({"message": "Suppliers listed successfully", "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def update_supplier(request):
    """
    Updates an existing supplier record.

    JSON Input:
    {
      "supplier_id": 1,  # Supplier ID to update
      "name": "Updated Supplier Name",
      "email": "updated_supplier@email.com",
      "phone": "9876543210",
      "address": "Updated Supplier Address"
    }

    Returns:
    200 OK with success message and updated supplier data on success,
    400 Bad Request with error details on validation failure,
    404 Not Found if the supplier record does not exist.
    """
    data = request.data  # JSON with updated supplier data
    supplier_id = data.get('supplier_id')  # Get the supplier ID from the JSON
    try:
        supplier = Supplier.objects.get(pk=supplier_id)
        serializer = SupplierSerializer(supplier, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Supplier updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"error": "Failed to update the supplier", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Supplier.DoesNotExist:
        return Response({"error": "Supplier not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_supplier(request):
    """
    Deletes an existing supplier record.

    JSON Input:
    {
      "supplier_id": 1  # Supplier ID to delete
    }

    Returns:
    204 No Content on successful deletion,
    404 Not Found if the supplier record does not exist.
    """
    data = request.data  # JSON with the supplier ID to delete
    supplier_id = data.get('supplier_id')  # Get the supplier ID from the JSON
    try:
        supplier = Supplier.objects.get(pk=supplier_id)
        supplier.delete()
        return Response({"message": "Supplier deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Supplier.DoesNotExist:
        return Response({"error": "Supplier not found"}, status=status.HTTP_404_NOT_FOUND)
