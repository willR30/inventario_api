from django.urls import path, include
from api.others.other_views import *

urlpatterns = [
    path('others/subtract_stock/',subtract_stock, name='subtract_stock'),
    path('others/customer_invoices', customer_invoices, name='customer_invoices'),
    path('others/invoices_by_specified_date_range/', invoices_by_specified_date_range, name='invoices_by_specified_date_range'),
    path('others/invoices_in_month/', invoices_in_month, name='invoices_in_month'),
    path('others/get_last_registered_invoice/', get_last_registered_invoice, name='get_last_registered_invoice'),
    path('others/get_currency_by_business/', get_currency_by_business, name='get_currency_by_business'),
    path('others/get_complete_invoce_number_series/', get_complete_invoice_number_series, name='get_complete_invoice_number_series'),

]