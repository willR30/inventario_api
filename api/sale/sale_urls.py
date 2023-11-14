from django.urls import path
from api.sale.sale_view_crud import *

urlpatterns = [
    path('create-sale/', create_sale, name='create-sale'),
    path('list-sales/', list_sales, name='list-sales'),
    path('update-sale/', update_sale, name='update-sale'),
    path('delete-sale/', delete_sale, name='delete-sale'),
]
