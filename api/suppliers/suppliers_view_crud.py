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
    Create a new supplier.

    This function is designed to create a new supplier, which requires a JSON with supplier data. 
    It checks if the JSON data is valid, saves the new supplier, and responds with a success message 
    along with the created supplier data. If there are validation errors in the data, it returns an error message with details.

    :param request: The HTTP request object.
    :return: Response with a success message and created supplier data if successful, or an error message with 
    validation errors if data is invalid.
    
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
    List suppliers associated with a specific business.

    This function expects to receive the 'business_id' as part of the JSON. 
    It lists all suppliers related to the specified business and responds with the results.

    :param request: The HTTP request object.
    :return: Response with a list of suppliers associated with the business or an error if no suppliers are found.
    
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
    Update an existing supplier.

    This function expects a JSON with updated supplier data and 'supplier_id' to identify the supplier to be updated. 
    If the update is successful, it responds with a success message and the updated supplier data. If there are validation 
    errors in the data, it returns an error message with details. If the supplier to update is not found, it returns an error.

    :param request: The HTTP request object.
    :return: Response with a success message and updated supplier data if the update is successful, or an error message 
    if the update fails or the supplier is not found.
    
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
    Delete a supplier.

    This function expects a JSON with the 'supplier_id' to identify the supplier to be deleted. 
    If the deletion is successful, it responds with a success message. If the supplier to delete is not found, 
    it returns an error.

    :param request: The HTTP request object.
    :return: Response with a success message if the supplier is deleted, or an error message if the supplier is not found.
    
    """
    data = request.data  # JSON with the supplier ID to delete
    supplier_id = data.get('supplier_id')  # Get the supplier ID from the JSON
    try:
        supplier = Supplier.objects.get(pk=supplier_id)
        supplier.delete()
        return Response({"message": "Supplier deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Supplier.DoesNotExist:
        return Response({"error": "Supplier not found"}, status=status.HTTP_404_NOT_FOUND)
