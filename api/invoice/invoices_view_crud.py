from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api.models import Invoice, Sale
from api.serializers import InvoiceSerializer
from api.views import get_business_id_by_user_from_server, increment_last_registered_invoice
from django.http import JsonResponse


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_invoice(request):
    """
    Creates a new invoice.

    JSON Input:
    {
      "invoice_number": "ABC123",
      "invoice_date": "2023-11-13T12:00:00Z",
      "sub_total": 100.0,
      "iva": 15.0,
      "total": 115.0,
      "customer": 1,  # Customer ID
      "business": 1,  # Business ID
      "payment_type": 1,  # PaymentType ID
      "sale": [{"product": 1, "quantity": 2, "cost_price_at_time": 7.0, "sale_price_at_time": 10.0}]
    }

    Returns:
    201 Created on success, 400 Bad Request on failure.
    """
    data = request.data
    serializer = InvoiceSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        increment_last_registered_invoice(request)#aumentamos la ultima factura en 1
        return Response({"message": "Invoice created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"error": "Failed to create the invoice", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_invoices(request):
    """
    Lists all invoices associated with the authenticated user's business.

    Returns:
    200 OK with invoice data on success.
    """
    business = get_business_id_by_user_from_server(request)
    invoices = Invoice.objects.filter(business_id=business)

    invoices_list = []
    for invoice in invoices:
        invoice_data = {
            'invoice_id': invoice.id,
            'invoice_number': invoice.invoice_number,
            'invoice_date': invoice.invoice_date.strftime('%Y-%m-%d %H:%M:%S'),  # Format date as needed
            'sub_total': str(invoice.sub_total),
            'iva': str(invoice.iva),
            'total': str(invoice.total),
            'customer': {
                'first_name': invoice.customer.first_name,
                'last_name': invoice.customer.last_name,
                'email': invoice.customer.email,
                'phone': invoice.customer.phone,
                'c_address': invoice.customer.c_address,
                # Add other customer fields as needed
            },
            'business': {
                'business_id': invoice.business.id,
                'business_name': invoice.business.name,
                # Add other business fields as needed
            },
            'payment_type': {
                'payment_type_id': invoice.payment_type.id,
                'payment_type_name': invoice.payment_type.name,
                # Add other payment type fields as needed
            },
            'sales': []  # List to store sales associated with the invoice
        }

        # Fetch sales related to the invoice
        sales = Sale.objects.filter(invoice=invoice)
        for sale in sales:
            sale_data = {
                'product_id': sale.product.id,
                'product_name': sale.product.name,
                'quantity': sale.quantity,
                'cost_price_at_time': str(sale.cost_price_at_time),
                'sale_price_at_time': str(sale.sale_price_at_time),
                # Add other sale fields as needed
            }
            invoice_data['sales'].append(sale_data)

        invoices_list.append(invoice_data)

    return JsonResponse({"message": "Invoices listed successfully", "data": invoices_list}, status=200)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_invoice(request):
    """
    Updates an existing invoice.

    JSON Input:
    {
      "invoice_id": 1,  # Invoice ID to update
      "invoice_number": "Updated_ABC123",
      "invoice_date": "2023-11-14T12:00:00Z",
      "sub_total": 120.0,
      "iva": 18.0,
      "total": 138.0,
      "customer": 2  # Updated Customer ID
    }

    Returns:
    200 OK with updated invoice data on success, 400 Bad Request on failure, 404 Not Found if the invoice doesn't exist.
    """
    data = request.data
    invoice_id = data.get('invoice_id')
    try:
        invoice = Invoice.objects.get(pk=invoice_id)
        serializer = InvoiceSerializer(invoice, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Invoice updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"error": "Failed to update the invoice", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Invoice.DoesNotExist:
        return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_invoice(request):
    """
    Deletes an invoice.

    JSON Input:
    {
      "invoice_id": 1  # Invoice ID to delete
    }

    Returns:
    204 No Content on success, 404 Not Found if the invoice doesn't exist.
    """
    data = request.data
    invoice_id = data.get('invoice_id')
    try:
        invoice = Invoice.objects.get(pk=invoice_id)
        invoice.delete()
        return Response({"message": "Invoice deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Invoice.DoesNotExist:
        return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_total_all_for_invoice(request):
    """
    Retrieves the total sales amount for all invoices associated with the authenticated user's business.

    Returns:
    200 OK with the total sales amount on success.
    """
    business_id = get_business_id_by_user_from_server(request)
    total = 0
    invoices = Invoice.objects.filter(business=business_id)
    for i in invoices:
        total += i.total
    return Response({"total_sales": total}, status=status.HTTP_200_OK)
