from django.urls import path
from api.products_category.product_category_view_crud import *

urlpatterns = [
    #import product category
    path('create-product-category/', create_product_category, name='create-product-category'),
    path('list-product-categories/', list_product_categories, name='list-product-categories'),
    path('update-product-category/', update_product_category, name='update-product-category'),
    path('delete-product-category/', delete_product_category, name='delete-product-category'),
]
