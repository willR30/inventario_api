from django.urls import path
from api.invoice.invoices_view_crud import *

urlpatterns = [
    path('create-invoice/', create_invoice, name='create-invoice'),
    path('list-invoices/', list_invoices, name='list-invoices'),
    path('update-invoice/', update_invoice, name='update-invoice'),
    path('delete-invoice/', delete_invoice, name='delete-invoice'),
    path('total-sales-invoice/', get_total_all_for_invoice, name='total_sales'),
]
