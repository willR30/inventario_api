from rest_framework import viewsets, generics, permissions
from django.contrib.auth.models import User
from api.serializers import UserSerializer, BusinessSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny, IsAuthenticated  # Cambio en la importación
from django.db.models import Q
from api.models import Business, PlanType, Currency


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
def register_user_with_business(request):
    """
        Register a new user and associate them with a business.

        This endpoint allows for the registration of a new user along with the creation of a business
        associated with that user. Both user and business data should be provided in the request JSON.

        Parameters:
        - user (object): User data for registration. Fields may include:
          - username (string): User's username.
          - password (string): User's password.

        - business (object): Business data to create a business associated with the user. Fields may include:
          - name (string): Business name.
          - photo_link (string): Link to business photo (optional).
          - authorization_number (string): Business authorization number.
          - invoice_series (string): Invoice series.
          - invoice_number (integer): Invoice number.
          - last_registered_invoice (integer): this is a copy from the plan type that user choose in that moment
          - number_of_product_records_available (integer): Number of product records available.
          - plan_type_id (integer): ID of the associated plan type.
          - currency_id (integer): ID of the associated currency.

        Returns:
        - 201 Created: If the user and business are successfully registered.
        - 400 Bad Request: If there are validation errors or a failure in user/business registration.
        - 405 Method Not Allowed: If an invalid request method is used.

        Permission:
        - AllowAny: Access is allowed without authentication.

        Example Request:
        ```
        POST /register-user-with-business/
        {
          "user": {
            "username": "newuser",
            "password": "password123"
          },
          "business": {
            "name": "My Business",
            "authorization_number": "123456",
            "invoice_series": "A",
            "invoice_number": 1000,
            "number_of_product_records_available": 500,
            "plan_type": 1,
            "currency": 1
          }
        }
        ```

        Example Response:
        ```
        HTTP/1.1 201 Created
        {
          "message": "User and business registered successfully"
        }
    """
    if request.method == 'POST':
        user_data = request.data.get('user', {})  # Obtén los datos del usuario del JSON
        business_data = request.data.get('business', {})  # Obtén los datos del negocio del JSON

        # Crea el usuario
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            # Obtiene el valor de "max_product_record_count" del PlanType
            plan_type_id = business_data.get('plan_type')
            try:
                plan_type = PlanType.objects.get(id=plan_type_id)
            except PlanType.DoesNotExist:
                return Response({"error": "PlanType not found"}, status=status.HTTP_404_NOT_FOUND)

            # Crea el negocio relacionado con el usuario
            business_data['user'] = user.id  # Asocia el usuario al negocio
            business_data['number_of_product_records_available'] = plan_type.max_product_record_count #pasamos el valor como parámetro
            business_data['last_registered_invoice'] = "0"
            business_serializer = BusinessSerializer(data=business_data)

            if business_serializer.is_valid():
                business_serializer.save()
                return Response({"message": "User and business registered successfully"}, status=status.HTTP_201_CREATED)
            else:
                user.delete()  # Elimina el usuario si falla la creación del negocio
                return Response({"error": "Failed to create the business", "business_errors": business_serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Failed to create the user", "user_errors": user_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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
