from django.urls import path, include
from api.user.user_view_autentication import *

urlpatterns = [
    #autenticación rutas
    path('user/register/', register_user, name='register'),
    path('user/login/', user_login, name='login'),
    path('user/logout/', user_logout, name='logout'),

]