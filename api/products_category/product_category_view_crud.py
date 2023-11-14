# api/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from api.models import ProductCategory
from api.serializers import ProductCategorySerializer
from api.views import get_business_id_by_user_from_server
from rest_framework.authentication import TokenAuthentication


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_product_category(request):
    """
    Creates a new product category.

    JSON Input:
    {
      "name": "Fruits",  # Category name
      "icon_link": "http://example.com/icon.jpg"  # URL of the category icon image
    }

    Returns:
    201 Created with success message and category data on success,
    400 Bad Request with error details on validation failure.
    """
    data = request.data  # JSON with data for the new product category
    serializer = ProductCategorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Product category created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"error": "Failed to create the product category", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_product_categories(request):
    """
    Lists product categories associated with the authenticated user's business.

    Returns:
    200 OK with product category data on success.
    """
    business = get_business_id_by_user_from_server(request)
    product_categories = ProductCategory.objects.filter(business_id=business)
    serializer = ProductCategorySerializer(product_categories, many=True)
    return Response({"message": "Product categories listed successfully", "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_product_category(request):
    """
    Updates an existing product category.

    JSON Input:
    {
      "product_category_id": 1,  # Product category ID
      "name": "Vegetables",  # Updated category name
      "icon_link": "http://example.com/updated_icon.jpg"  # Updated URL of the category icon image
    }

    Returns:
    200 OK with success message and updated category data on success,
    400 Bad Request with error details on validation failure,
    404 Not Found if the product category does not exist.
    """
    data = request.data  # JSON with updated product category data
    product_category_id = data.get('product_category_id')  # Get the product category ID from the JSON
    try:
        product_category = ProductCategory.objects.get(pk=product_category_id)
        serializer = ProductCategorySerializer(product_category, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product category updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"error": "Failed to update the product category", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except ProductCategory.DoesNotExist:
        return Response({"error": "Product category not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_product_category(request):
    """
    Deletes an existing product category.

    JSON Input:
    {
      "product_category_id": 1  # Product category ID to delete
    }

    Returns:
    204 No Content on successful deletion,
    404 Not Found if the product category does not exist.
    """
    data = request.data  # JSON with the product category ID to delete
    product_category_id = data.get('product_category_id')  # Get the product category ID from the JSON
    try:
        product_category = ProductCategory.objects.get(pk=product_category_id)
        product_category.delete()
        return Response({"message": "Product category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except ProductCategory.DoesNotExist:
        return Response({"error": "Product category not found"}, status=status.HTTP_404_NOT_FOUND)
