from django.urls import path
from api.suppliers.suppliers_view_crud import *

urlpatterns = [
    path('create-supplier/', create_supplier, name='create-supplier'),
    path('list-suppliers/', list_suppliers, name='list-suppliers'),
    path('update-supplier/', update_supplier, name='update-supplier'),
    path('delete-supplier/', delete_supplier, name='delete-supplier'),
]



