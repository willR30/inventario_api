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
    Create a new product category.

    This function expects a JSON with product category data to create a new product category. 
    If the product category is created successfully, it responds with a success message and the product category data. 
    If there are validation errors in the data, it returns an error message with details.

    :param request: The HTTP request object.
    :return: Response with a success message and product category data if the product category is created, or an error message 
    if creation fails.
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
    List product categories associated with a specific business.

    This function expects to receive the 'business_id' as part of the JSON. It lists all product categories related to 
    the specified business and responds with the results.

    :param request: The HTTP request object.
    :return: Response with a list of product categories associated with the business or an error if no product categories 
    are found.
    
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
    Update an existing product category.

    This function expects a JSON with updated product category data and 'product_category_id' to identify the product category 
    to be updated. If the update is successful, it responds with a success message and the updated product category data. 
    If there are validation errors in the data, it returns an error message with details. If the product category to update 
    is not found, it returns an error.

    :param request: The HTTP request object.
    :return: Response with a success message and updated product category data if the update is successful, or an error message 
    if the update fails or the product category is not found.
    
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
    Delete a product category.

    This function expects a JSON with the 'product_category_id' to identify the product category to be deleted.
    If the deletion is successful, it responds with a success message. If the product category to delete is not found,
    it returns an error.

    :param request: The HTTP request object.
    :return: Response with a success message if the product category is deleted, or an error message if the product category
    is not found.
    
    """
    data = request.data  # JSON with the product category ID to delete
    product_category_id = data.get('product_category_id')  # Get the product category ID from the JSON
    try:
        product_category = ProductCategory.objects.get(pk=product_category_id)
        product_category.delete()
        return Response({"message": "Product category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except ProductCategory.DoesNotExist:
        return Response({"error": "Product category not found"}, status=status.HTTP_404_NOT_FOUND)
