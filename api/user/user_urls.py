from django.urls import path, include
from api.user.user_view_autentication import *

urlpatterns = [
    #autenticación rutas
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register-user-with-business/', register_user_with_business, name='register_user_with_business'),
    path('register-randon-user/', register_randon_user, name='register_randon_user'),
    path('register-randon-user-with-email-and-business/', register_randon_user_with_email_and_business, name='register_randon_user_with_email_and_business'),

]