from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated  # Cambio en la importación
from django.db.models import Q
from api.models import Product, Invoice, Business
from api.serializers import InvoiceSerializer


# endpoint adicionales
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def restar_stock(request):
    """
    Reduce the stock quantity of a product by the specified amount.

    This function expects a JSON with 'product_id' and 'quantity' to perform the stock reduction. If the operation is successful, it responds with a success message. If the product doesn't exist or the stock is insufficient, it returns an error.

    :param request: The HTTP request object.
    :return: Response with a success message if the stock is updated, or an error if the product doesn't exist or there's insufficient stock.
    
    """
    if request.method == 'POST':
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        try:
            product = Product.objects.get(pk=product_id)
            if product.stock >= quantity:
                product.stock -= quantity
                product.save()
                return Response({'message': 'Stock actualizado correctamente.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No hay suficiente stock disponible.'}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({'error': 'El producto no existe.'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Método no permitido.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def facturas_de_cliente(request):
    """
    List all invoices associated with a specific customer.

    This function expects to receive the 'cliente_id' as part of the JSON.

    :param request: The HTTP request object.
    :return: Response with a list of invoices associated with the customer or an error if no invoices are found.
    
    """
    if request.method == 'POST':
        cliente_id = request.data.get('cliente_id')
        try:
            facturas = Invoice.objects.filter(customer=cliente_id)
            # Puedes serializar las facturas aquí si deseas enviar datos serializados como respuesta
            serializer = InvoiceSerializer(facturas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            # return Response(facturas.values(), status=status.HTTP_200_OK)
        except Invoice.DoesNotExist:
            return Response({'error': 'No se encontraron facturas para el cliente especificado.'},
                            status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Método no permitido.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def facturas_en_rango(request):
    """
    List invoices within a date range.

    This function expects to receive a JSON with 'rango_fechas' that contains 'fecha_inicio' (start date) and 'fecha_fin' (end date). The function lists invoices within the specified date range and responds with the results.

    :param request: The HTTP request object.
    :return: Response with invoices within the specified date range or an error if no invoices are found.
    
    """
    if request.method == 'POST':
        rango_fechas = request.data.get('rango_fechas', None)

        if rango_fechas and 'fecha_inicio' in rango_fechas and 'fecha_fin' in rango_fechas:
            fecha_inicio = rango_fechas['fecha_inicio']
            fecha_fin = rango_fechas['fecha_fin']

            try:
                facturas = Invoice.objects.filter(
                    Q(invoice_date__gte=fecha_inicio) & Q(invoice_date__lte=fecha_fin)
                )
                # Puedes serializar las facturas aquí si deseas enviar datos serializados como respuesta
                serializer = InvoiceSerializer(facturas, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
                # return Response(facturas.values(), status=status.HTTP_200_OK)
            except Invoice.DoesNotExist:
                return Response({'error': 'No se encontraron facturas en el rango especificado.'},
                                status=status.HTTP_404_NOT_FOUND)

        return Response({'error': 'Los parámetros de fecha son obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Método no permitido.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def facturas_en_mes(request):
    """
    List invoices for a specific month.

    This function expects to receive the 'mes' as part of the JSON. The function lists invoices for the specified month and responds with the results.

    :param request: The HTTP request object.
    :return: Response with invoices for the specified month or an error if no invoices are found.
    
    """
    if request.method == 'POST':
        mes = request.data.get('mes', None)

        if mes:
            try:
                facturas = Invoice.objects.filter(invoice_date__month=mes)
                # Puedes serializar las facturas aquí si deseas enviar datos serializados como respuesta
                serializer = InvoiceSerializer(facturas, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Invoice.DoesNotExist:
                return Response({'error': 'No se encontraron facturas para el mes especificado.'},
                                status=status.HTTP_404_NOT_FOUND)

        return Response({'error': 'El parámetro de mes es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Método no permitido.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_last_registered_invoice(request):
    """
    Retrieve the last registered invoice number for a specific business.

    This function expects to receive the 'business_id' as part of the JSON and retrieves the last registered invoice number for that business.

    :param request: The HTTP request object.
    :return: Response with the last registered invoice number or an error if the business is not found.
    """
    try:
        business_id = request.data.get('business_id')  # Obtiene el ID del negocio del JSON
        business = Business.objects.get(id=business_id)
        last_invoice = business.last_registered_invoice
        return Response({'last_registered_invoice': last_invoice}, status=status.HTTP_200_OK)
    except Business.DoesNotExist:
        return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_currency_by_business(request):
    """
    Retrieve currency information for a specific business.

    This function expects to receive the 'business_id' as part of the JSON and retrieves the currency details associated with that business.

    :param request: The HTTP request object.
    :return: Response with currency details for the business or an error if the business is not found.
    """
    try:
        business_id = request.data.get('business_id')  # Obtiene el ID del negocio del JSON
        business = Business.objects.get(id=business_id)
        currency = business.currency
        return Response({'currency': currency.name,
                         'symbol': currency.symbol,
                         'international identifier': currency.international_identifier
                         }, status=status.HTTP_200_OK)
    except Business.DoesNotExist:
        return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_complete_invoice_number_series(request):
    """
    Retrieve the concatenated information of authorization number, invoice series, and invoice number for a specific business.

    This function expects to receive the 'business_id' as part of the JSON and retrieves and concatenates the information of authorization number, invoice series, and invoice number.

    :param request: The HTTP request object.
    :return: Response with the concatenated information or an error if the business is not found.
    """
    try:
        business_id = request.data.get('business_id')  # Obtiene el ID del negocio del JSON
        business = Business.objects.get(id=business_id)

        # Concatena los valores en una sola cadena
        concatenated_info = f"{business.authorization_number} {business.invoice_series} {business.invoice_number}"

        return Response({'concatenated_info': concatenated_info}, status=status.HTTP_200_OK)
    except Business.DoesNotExist:
        return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)
