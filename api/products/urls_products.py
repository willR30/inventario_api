from django.urls import path
from .products_view_crud import *

urlpatterns = [
        path('create-product/', create_product, name='create-product'),
        path('list-products/', list_products_by_business, name='list-products'),
        path('update-product/', update_product, name='update-product'),
        path('delete-product/', delete_product, name='delete-product'),
        path('search-product-by-name/', search_products_by_name, name='search-product-name'),
        path('get_product_by_category/', get_business_id_by_user_from_server, name="get_products_by_category"),
        
]
