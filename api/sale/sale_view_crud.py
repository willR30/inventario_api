from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from api.models import Sale, Product
from api.serializers import SaleSerializer
from api.views import get_business_id_by_user_from_server
from rest_framework.authentication import TokenAuthentication


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_sale(request):
    """
    Creates a new sale record.

    JSON Input:
    {
      "product": 1,  # Product ID for the sale
      "quantity": 5  # Quantity of the product sold
    }

    Returns:
    201 Created with success message on successful sale creation,
    400 Bad Request with error details if the product or quantity is invalid,
    404 Not Found if the specified product does not exist.
    """
    if request.method == 'POST':
        data = request.data

        # Verify if the product exists
        product_id = data.get('product')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Verify if there is sufficient inventory for the sale
        quantity = data.get('quantity')
        if product.stock < quantity:
            return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the sale record
        sale = Sale(product=product, quantity=quantity, cost_price_at_time=product.cost_price, sale_price_at_time=product.sale_price)
        sale.save()

        # Update the product inventory
        product.stock -= quantity
        product.save()

        return Response({'message': 'Sale created successfully'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_sales(request):
    """
    Lists sales associated with the authenticated user's business.

    Returns:
    200 OK with sale data on success.
    """
    business = get_business_id_by_user_from_server(request)
    sales = Sale.objects.filter(invoice__business_id=business)
    serializer = SaleSerializer(sales, many=True)
    return Response({"message": "Sales listed successfully", "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_sale(request):
    """
    Updates an existing sale record.

    JSON Input:
    {
      "sale_id": 1,  # Sale ID to update
      "quantity": 8  # Updated quantity of the product sold
    }

    Returns:
    200 OK with success message and updated sale data on success,
    400 Bad Request with error details on validation failure,
    404 Not Found if the sale record does not exist.
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_sale(request):
    """
    Deletes an existing sale record.

    JSON Input:
    {
      "sale_id": 1  # Sale ID to delete
    }

    Returns:
    204 No Content on successful deletion,
    404 Not Found if the sale record does not exist.
    """
    data = request.data  # JSON with the sale ID to delete
    sale_id = data.get('sale_id')  # Get the sale ID from the JSON
    try:
        sale = Sale.objects.get(pk=sale_id)
        sale.delete()
        return Response({"message": "Sale deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Sale.DoesNotExist:
        return Response({"error": "Sale not found"}, status=status.HTTP_404_NOT_FOUND)


