from django.urls import path, include
from api.others.other_views import *

urlpatterns = [
    path('subtract_stock/', subtract_stock, name='subtract_stock'),
    path('customer_invoices', customer_invoices, name='customer_invoices'),
    path('invoices_by_specified_date_range/', invoices_by_specified_date_range,
         name='invoices_by_specified_date_range'),
    path('invoices_in_month/', invoices_in_month, name='invoices_in_month'),
    path('get_last_registered_invoice/', get_last_registered_invoice, name='get_last_registered_invoice'),
    path('get_currency_by_business/', get_currency_by_business, name='get_currency_by_business'),
    path('get_complete_invoice_number_series/', get_complete_invoice_number_series,
         name='get_complete_invoice_number_series'),
    path('update_business_name_and_photo', edit_name_photo_for_business, name='edit_name_photo_for_business')
]
