# api/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from api.models import Sale, Product
from api.serializers import SaleSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_sale(request):
    """
    Create a new sale.

    This function is designed to create a new sale, which requires a JSON with sale data. 
    It first checks if the specified product exists and if there is sufficient stock for the sale. 
    If the product exists and there's enough stock, it creates a sale record and updates the product's stock. 
    If successful, it responds with a success message.

    :param request: The HTTP request object.
    :return: Response with a success message if the sale is created, or an error message 
    if the product doesn't exist or there's insufficient stock.
    
    """
    if request.method == 'POST':
        data = request.data

        # Verificar si el producto existe
        product_id = data.get('product')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Verificar si hay suficiente inventario para la venta
        quantity = data.get('quantity')
        if product.stock < quantity:
            return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)

        # Crear el registro de venta
        sale = Sale(product=product, quantity=quantity)
        sale.save()

        # Actualizar el inventario del producto
        product.stock -= quantity
        product.save()

        return Response({'message': 'Sale created successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def list_sales(request):
    """
    List sales associated with a specific business.

    This function expects to receive the 'business_id' as part of the JSON. It lists all sales related to the 
    specified business and responds with the results.

    :param request: The HTTP request object.
    :return: Response with a list of sales associated with the business or an error if no sales are found.
    
    """
    business_id = request.data.get('business_id')  # Business ID
    sales = Sale.objects.filter(invoice__business__id=business_id)
    serializer = SaleSerializer(sales, many=True)
    return Response({"message": "Sales listed successfully", "data": serializer.data}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_sale(request):
    """
    Update an existing sale.

    This function expects a JSON with updated sale data and 'sale_id' to identify the sale to be updated. 
    If the update is successful, it responds with a success message and the updated sale data. If there are 
    validation errors in the data, it returns an error message with details. If the sale to update is not found, 
    it returns an error.

    :param request: The HTTP request object.
    :return: Response with a success message and updated sale data if the update is successful, or an error message if the update fails or the sale is not found.
    
    """
    data = request.data  # JSON with updated sale data
    sale_id = data.get('sale_id')  # Get the sale ID from the JSON
    try:
        sale = Sale.objects.get(pk=sale_id)
        serializer = SaleSerializer(sale, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Sale updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"error": "Failed to update the sale", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Sale.DoesNotExist:
        return Response({"error": "Sale not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_sale(request):
    """
    Delete a sale.

    This function expects a JSON with the 'sale_id' to identify the sale to be deleted. 
    If the deletion is successful, it responds with a success message. If the sale to delete is not found, it returns an error.

    :param request: The HTTP request object.
    :return: Response with a success message if the sale is deleted, or an error message if the sale is not found.
    
    """
    data = request.data  # JSON with the sale ID to delete
    sale_id = data.get('sale_id')  # Get the sale ID from the JSON
    try:
        sale = Sale.objects.get(pk=sale_id)
        sale.delete()
        return Response({"message": "Sale deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Sale.DoesNotExist:
        return Response({"error": "Sale not found"}, status=status.HTTP_404_NOT_FOUND)
