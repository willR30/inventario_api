from django.urls import path
from api.customers.customers_view_crud import *

urlpatterns = [
        #import Customers url
    path('create-customer/', create_customer, name='create-customer'),
    path('list-customers/', list_customers, name='list-customers'),
    path('update-customer/', update_customer, name='update-customer'),
    path('delete-customer/', delete_customer, name='delete-customer'),

]