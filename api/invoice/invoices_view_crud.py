# api/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from api.models import Invoice
from api.serializers import InvoiceSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_invoice(request):
    """
    Create a new invoice in the database.

    This function expects to receive a JSON with the invoice's data. The function validates the data and responds with a success message if the creation is successful.

    :param request: The HTTP request object.
    :return: Response with success message and data of the created invoice.
    """
    data = request.data  # JSON with data for the new invoice
    serializer = InvoiceSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Invoice created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"error": "Failed to create the invoice", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def list_invoices(request):
    """
    List all invoices associated with a specific business.

    This function expects to receive the business's ID as part of the JSON.

    :param request: The HTTP request object.
    :return: Response with success message and a list of invoices associated with the business.
    """
    business_id = request.data.get('business_id')  # Business ID
    invoices = Invoice.objects.filter(business__id=business_id)
    serializer = InvoiceSerializer(invoices, many=True)
    return Response({"message": "Invoices listed successfully", "data": serializer.data}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_invoice(request):
    """
    Update the information of an existing invoice in the database.

    This function expects to receive a JSON with the updated invoice data, including the ID of the invoice to be updated.

    :param request: The HTTP request object.
    :return: Response with success message and the data of the updated invoice.
    """
    data = request.data  # JSON with updated invoice data
    invoice_id = data.get('invoice_id')  # Get the invoice ID from the JSON
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
@permission_classes([IsAuthenticated])
def delete_invoice(request):
    """
    Delete an invoice from the database.

    This function expects to receive the ID of the invoice to be deleted as part of the JSON.

    :param request: The HTTP request object.
    :return: Response with a success message confirming the deletion.
    """
    data = request.data  # JSON with the invoice ID to delete
    invoice_id = data.get('invoice_id')  # Get the invoice ID from the JSON
    try:
        invoice = Invoice.objects.get(pk=invoice_id)
        invoice.delete()
        return Response({"message": "Invoice deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Invoice.DoesNotExist:
        return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)
