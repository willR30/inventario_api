from rest_framework import viewsets, generics, permissions
from django.contrib.auth.models import User
from api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny, IsAuthenticated  # Cambio en la importación
from django.db.models import Q
from api.models import Business


# Configuración de permisos para las vistas de registro e inicio de sesión
@api_view(['POST'])
@permission_classes([AllowAny])  # Permite el acceso sin autenticación
def register_user(request):
    """
    Register a new user.

    This function allows the registration of a new user with the provided data in the request. 
    If the registration is successful, it returns the user data and a token. 
    
    If there are validation errors in the data, it returns an error message with details.

    :param request: The HTTP request object.
    :return: Response with user data and a token if the registration is successful, 
    or an error message with validation errors if data is invalid.
    
    """
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])  # Permite el acceso sin autenticación
def user_login(request):
    """
    Log in a user.

    This function allows a user to log in using their credentials (username and password) or email and password. 
    If the login is successful, it returns the user's ID, a token, and business data if applicable. If the login fails, 
    it returns an error message.

    :param request: The HTTP request object.
    :return: Response with user data, token, and business data if the login is successful, or an error message if the login fails.
    
    """
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)

            try:
                business = Business.objects.get(user=user)
                business_data = {
                    'id': business.id,
                    'name': business.name,
                    'photo_link': business.photo_link,
                    'authorization_number': business.authorization_number,
                    'invoice_series': business.invoice_series,
                    'invoice_number': business.invoice_number,
                    'last_registered_invoice': business.last_registered_invoice,
                    'number_of_product_records_available': business.number_of_product_records_available,
                    'plan_type_id': business.plan_type_id,  # ID del tipo de plan vinculado al negocio
                    'currency_id': business.currency_id  # ID de la moneda vinculada al negocio
                }

            except Business.DoesNotExist:
                business_data = None

            return Response({
                'user_id': user.id,
                'token': token.key,
                'business': business_data  # Incluye detalles del negocio en la respuesta
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# Configuración de permisos para la vista de cierre de sesión
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Permite el acceso solo a usuarios autenticados
def user_logout(request):
    """
    Log out a user.

    This function allows a logged-in user to log out. 
    If the logout is successful, it returns a success message. If the logout fails, it returns an error message.

    :param request: The HTTP request object.
    :return: Response with a success message if the logout is successful, or an error message if the logout fails.
    
    """
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
