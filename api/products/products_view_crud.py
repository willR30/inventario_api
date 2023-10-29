from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from api.models import Product, Business
from api.serializers import ProductSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    """
    Create a new product.

    This function expects a JSON with product data to create a new product. If the product is created successfully,
    it responds with a success message and the product data. If there are validation errors in the data, it returns an error
    message with details.

    :param request: The HTTP request object.
    :return: Response with a success message and product data if the product is created, or an error message if creation fails.
    
    """
    data = request.data  # JSON with data for the new product
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Product created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"error": "Failed to create the product", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def list_products_by_business(request):
    """
    List products associated with a specific business.

    This function expects to receive the 'business_id' as part of the JSON. It lists all products
    related to the specified business and responds with the results.

    :param request: The HTTP request object.
    :return: Response with a list of products associated with the business or an error if no products are found.
    
    """
    business_id = request.data.get('business_id')  # Business ID
    products = Product.objects.filter(business__id=business_id)
    serializer = ProductSerializer(products, many=True)
    return Response({"message": "Products listed successfully", "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request):
    """
    Update an existing product.

    This function expects a JSON with updated product data and 'product_id' to identify the product to be updated. 
    If the update is successful, it responds with a success message and the updated product data. If there are validation errors in the data, it returns an error message with details. If the product to update is not found, it returns an error.

    :param request: The HTTP request object.
    :return: Response with a success message and updated product data if the update is successful, or an error message 
    if the update fails or the product is not found.
    
    """
    data = request.data  # JSON con datos actualizados del producto
    product_id = data.get('product_id')  # Obtén el ID del producto desde el JSON
    try:
        product = Product.objects.get(pk=product_id)
        serializer = ProductSerializer(product, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"error": "Failed to update the product", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request):
    """
    Delete a product.

    This function expects a JSON with the 'product_id' to identify the product to be deleted. If the deletion is successful, 
    it responds with a success message. If the product to delete is not found, it returns an error.

    :param request: The HTTP request object.
    :return: Response with a success message if the product is deleted, or an error message if the product is not found.
    
    """
    data = request.data  # JSON con el ID del producto a eliminar
    product_id = data.get('product_id')  # Obtén el ID del producto desde el JSON
    try:
        product = Product.objects.get(pk=product_id)
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)





@api_view(['POST'])
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
