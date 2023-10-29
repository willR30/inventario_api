from django.urls import path, include
from api.others.other_views import *

urlpatterns = [
     # Otras rutas
    path('others/restar-stock/',restar_stock, name='restar-stock'),
    path('others/facturas-de-cliente/',facturas_de_cliente, name='facturas-de-cliente'),
    path('others/facturas-en-rango/', facturas_en_rango, name='facturas-en-rango'),
    path('others/facturas-en-mes/', facturas_en_mes, name='facturas-en-mes'),
    path('others/get_last_registered_invoice/', get_last_registered_invoice, name='get_last_registered_invoice'),
    path('others/get_currency_by_business/', get_currency_by_business, name='get_currency_by_business'),
    path('others/get_complete_invoce_number_series/', get_complete_invoice_number_series, name='get_complete_invoice_number_series'),

]