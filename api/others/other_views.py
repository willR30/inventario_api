from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated  # Cambio en la importación
from django.db.models import Q
from api.models import Product, Invoice, Business
from api.serializers import InvoiceSerializer
from api.views import get_business_id_by_user_from_server

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def subtract_stock(request):
    """
    Subtracts the specified quantity from the stock of a product.

    JSON Input:
    {
      "product_id": 1,  # Product ID
      "quantity": 5
    }

    Returns:
    200 OK with a success message on successful stock update,
    400 Bad Request if there is insufficient stock,
    404 Not Found if the product doesn't exist.
    """
    if request.method == 'POST':
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        try:
            product = Product.objects.get(pk=product_id)
            if product.stock >= quantity:
                product.stock -= quantity
                product.save()
                return Response({'message': 'Stock updated successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Insufficient stock available.'}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({'error': 'Product does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def customer_invoices(request):
    """
    Retrieves invoices associated with a specified customer.

    JSON Input:
    {
      "customer_id": 1  # Customer ID
    }

    Returns:
    200 OK with invoice data on success,
    404 Not Found if no invoices are found for the specified customer.
    """
    if request.method == 'POST':
        customer_id = request.data.get('customer_id')
        try:
            invoices = Invoice.objects.filter(customer=customer_id)
            serializer = InvoiceSerializer(invoices, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Invoice.DoesNotExist:
            return Response({'error': 'No invoices found for the specified customer.'},
                            status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def invoices_by_specified_date_range(request):
    """
    Retrieves invoices within a specified date range.

    JSON Input:
    {
      "rango_fechas": {
        "fecha_inicio": "2023-01-01T00:00:00Z",
        "fecha_fin": "2023-12-31T23:59:59Z"
      }
    }

    Returns:
    200 OK with invoice data on success,
    404 Not Found if no invoices are found within the specified date range,
    400 Bad Request if date parameters are missing.
    """
    if request.method == 'POST':
        date_range = request.data.get('rango_fechas', None)

        if date_range and 'fecha_inicio' in date_range and 'fecha_fin' in date_range:
            start_date = date_range['fecha_inicio']
            end_date = date_range['fecha_fin']

            try:
                invoices = Invoice.objects.filter(
                    Q(invoice_date__gte=start_date) & Q(invoice_date__lte=end_date)
                )
                serializer = InvoiceSerializer(invoices, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Invoice.DoesNotExist:
                return Response({'error': 'No invoices found within the specified date range.'},
                                status=status.HTTP_404_NOT_FOUND)

        return Response({'error': 'Date parameters are mandatory.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def invoices_in_month(request):
    """
    Retrieves invoices for a specified month.

    JSON Input:
    {
      "mes": 1  # Month (1-12)
    }

    Returns:
    200 OK with invoice data on success,
    404 Not Found if no invoices are found for the specified month,
    400 Bad Request if the month parameter is missing.
    """
    if request.method == 'POST':
        month = request.data.get('mes', None)

        if month:
            try:
                invoices = Invoice.objects.filter(invoice_date__month=month)
                serializer = InvoiceSerializer(invoices, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Invoice.DoesNotExist:
                return Response({'error': 'No invoices found for the specified month.'},
                                status=status.HTTP_404_NOT_FOUND)

        return Response({'error': 'Month parameter is mandatory.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_last_registered_invoice(request):
    """
    Retrieves the last registered invoice number for the authenticated user's business.

    Returns:
    200 OK with the last registered invoice number on success,
    404 Not Found if the business is not found.
    """
    try:
        business = get_business_id_by_user_from_server(request)
        last_invoice = business.last_registered_invoice
        return Response({'last_registered_invoice': last_invoice}, status=status.HTTP_200_OK)
    except Business.DoesNotExist:
        return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_currency_by_business(request):
    """
    Retrieves the currency information for the authenticated user's business.

    Returns:
    200 OK with currency information on success,
    404 Not Found if the business is not found.
    """
    try:
        business = get_business_id_by_user_from_server(request)
        currency = business.currency
        return Response({'currency': currency.name,
                         'symbol': currency.symbol,
                         'international identifier': currency.international_identifier
                         }, status=status.HTTP_200_OK)
    except Business.DoesNotExist:
        return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_complete_invoice_number_series(request):
    """
    Retrieves the complete invoice number series for the authenticated user's business.

    Returns:
    200 OK with the concatenated invoice number series on success,
    404 Not Found if the business is not found.
    """
    try:
        business = get_business_id_by_user_from_server(request)

        # Concatenates the values into a single string
        concatenated_info = f"{business.authorization_number} {business.invoice_series} {business.invoice_number}"

        return Response({'concatenated_info': concatenated_info}, status=status.HTTP_200_OK)
    except Business.DoesNotExist:
        return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)







