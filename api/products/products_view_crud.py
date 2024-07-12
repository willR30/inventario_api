from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api.models import Product, Business
from api.serializers import ProductSerializer

from api.views import get_business_id_by_user_from_server, increment_register_available_for_business, decrement_register_available_for_business


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_product(request):
    """
    Creates a new product.

    JSON Input:
    {
      "photo_link": "url_to_product_photo",
      "name": "Product Name",
      "description": "Product Description",
      "stock": 10,
      "cost_price": 7.0,
      "sale_price": 10.0,
      "category": 1,  # ProductCategory ID
      "business": 1,  # Business ID
      "with_iva": true
    }

    Returns:
    201 Created on success, 400 Bad Request on failure.
    """
    data = request.data
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        product = serializer.save()
        if decrement_register_available_for_business(request):
            # Serializar el objeto guardado antes de devolverlo en la respuesta
            return Response({"message": "Product created successfully", "data": ProductSerializer(product).data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Failed to update business records"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Failed to create the product", "errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_products_by_business(request):
    """
    Lists all products associated with the authenticated user's business.

    Returns:
    200 OK with product data on success.
    """
    business = get_business_id_by_user_from_server(request)
    products = Product.objects.filter(business_id=business)
    serializer = ProductSerializer(products, many=True)
    return Response({"message": "Products listed successfully", "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_product(request):
    """
    Updates an existing product.

    JSON Input:
    {
      "product_id": 1,  # Product ID to update
      "photo_link": "updated_url_to_product_photo",
      "name": "Updated Product Name",
      "description": "Updated Product Description",
      "stock": 15,
      "cost_price": 8.0,
      "sale_price": 12.0,
      "category": 2  # Updated ProductCategory ID
    }

    Returns:
    200 OK with updated product data on success, 400 Bad Request on failure, 404 Not Found if the product doesn't exist.
    """
    data = request.data
    product_id = data.get('product_id')
    try:
        product = Product.objects.get(pk=product_id)
        serializer = ProductSerializer(product, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            increment_register_available_for_business(request)
            return Response({"message": "Product updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"error": "Failed to update the product", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_product(request):
    """
    Deletes a product.

    JSON Input:
    {
      "product_id": 1  # Product ID to delete
    }

    Returns:
    204 No Content on success, 404 Not Found if the product doesn't exist.
    """
    data = request.data
    product_id = data.get('product_id')
    try:
        product = Product.objects.get(pk=product_id)
        product.delete()
        decrement_register_available_for_business(request)
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def search_products_by_name(request):
    """
    Search for products by name with a partial match and filter by the user's associated business.
    This view allows you to search for products by a partial name match (case-insensitive) within the context
    of the user's associated business.
    Parameters:
    - request (Request): The HTTP request object containing the user's authentication and search query.

    Request JSON:
    - query (str): The search query for finding products by name.

    Returns:
    - Response: A JSON response containing the search results and an HTTP status code.

    Example JSON Response:
    {
        "message": "Products listed successfully",
        "data": [
            {
                "id": 1,
                "name": "Caramelos",
                "description": "Delicious candies",
                "price": "2.50",
                "stock": 100,
                "business": 1
            },
            {
                "id": 2,
                "name": "Carros",
                "description": "Toy cars for kids",
                "price": "12.99",
                "stock": 50,
                "business": 1
            },
            ...
        ]
    }

    Status Codes:
    - 200 OK: If the search is successful, and matching products are found.
    - 401 Unauthorized: If the user is not authenticated.
    - 404 Not Found: If the user's associated business does not exist.
    - 400 Bad Request: If the 'query' parameter is missing in the request or other errors occur.
    """
    user = request.user  # Obtener el usuario autenticado
    business = Business.objects.get(user=user)  # Obtener el negocio asociado al usuario

    # Obtener el parámetro "query" del JSON de la solicitud
    query = request.data.get('query', '')

    # Realizar la búsqueda de productos por coincidencia de nombre
    products = Product.objects.filter(
        business=business,
        name__icontains=query  # Realizar búsqueda por coincidencia de nombre (case-insensitive)
    )

    # Serializar los productos encontrados (usando tu serializador)
    serializer = ProductSerializer(products, many=True)

    return Response({"message": "Products listed successfully", "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_products_by_category(request):
    user = request.user  # Obtener el usuario autenticado
    business = Business.objects.get(user=user)  # Obtener el negocio asociado al usuario

    data = request.data
    category_id = data.get('category_id')
    print(category_id)
    # Realizar la búsqueda de productos por coincidencia de nombre
    products = Product.objects.filter(
       business_id=business, category=category_id
    )

    # Serializar los productos encontrados (usando tu serializador)
    serializer = ProductSerializer(products, many=True)

    return Response({"message": "Products listed successfully", "data": serializer.data}, status=status.HTTP_200_OK)

