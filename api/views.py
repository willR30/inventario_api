from rest_framework import viewsets, generics, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny, IsAuthenticated # Cambio en la importación
from django.db.models import Q

from django.contrib.auth import logout
from django.http import JsonResponse

from .models import PaymentType, Currency, PlanType, Business, UserRole, SubUserRegistration, ProductCategory, Product, Supplier, Customer, Invoice, Sale
from .serializers import PaymentTypeSerializer, CurrencySerializer, PlanTypeSerializer, BusinessSerializer, UserRoleSerializer, SubUserRegistrationSerializer, ProductCategorySerializer, ProductSerializer, SupplierSerializer, CustomerSerializer, InvoiceSerializer, SaleSerializer

class PaymentTypeViewSet(viewsets.ModelViewSet):
    queryset = PaymentType.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaymentTypeSerializer

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CurrencySerializer

class PlanTypeViewSet(viewsets.ModelViewSet):
    queryset = PlanType.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PlanTypeSerializer

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BusinessSerializer

class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserRoleSerializer

class SubUserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = SubUserRegistration.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubUserRegistrationSerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductCategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SupplierSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomerSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InvoiceSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SaleSerializer

# Configuración de permisos para las vistas de registro e inicio de sesión
@api_view(['POST'])
@permission_classes([AllowAny])  # Permite el acceso sin autenticación
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])  # Permite el acceso sin autenticación
def user_login(request):
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
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'You have been logged out.'})




#endpoint adicionales
@api_view(['POST'])
def restar_stock(request):
    if request.method == 'POST':
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        try:
            product = Product.objects.get(pk=product_id)
            if product.stock >= quantity:
                product.stock -= quantity
                product.save()
                return Response({'message': 'Stock actualizado correctamente.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No hay suficiente stock disponible.'}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({'error': 'El producto no existe.'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Método no permitido.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def facturas_de_cliente(request):
    if request.method == 'POST':
        cliente_id = request.data.get('cliente_id')
        try:
            facturas = Invoice.objects.filter(customer=cliente_id)
            # Puedes serializar las facturas aquí si deseas enviar datos serializados como respuesta
            serializer = InvoiceSerializer(facturas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            #return Response(facturas.values(), status=status.HTTP_200_OK)
        except Invoice.DoesNotExist:
            return Response({'error': 'No se encontraron facturas para el cliente especificado.'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Método no permitido.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def facturas_en_rango(request):
    if request.method == 'POST':
        rango_fechas = request.data.get('rango_fechas', None)

        if rango_fechas and 'fecha_inicio' in rango_fechas and 'fecha_fin' in rango_fechas:
            fecha_inicio = rango_fechas['fecha_inicio']
            fecha_fin = rango_fechas['fecha_fin']

            try:
                facturas = Invoice.objects.filter(
                    Q(invoice_date__gte=fecha_inicio) & Q(invoice_date__lte=fecha_fin)
                )
                # Puedes serializar las facturas aquí si deseas enviar datos serializados como respuesta
                serializer = InvoiceSerializer(facturas, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
                #return Response(facturas.values(), status=status.HTTP_200_OK)
            except Invoice.DoesNotExist:
                return Response({'error': 'No se encontraron facturas en el rango especificado.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'error': 'Los parámetros de fecha son obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Método no permitido.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['POST'])
def facturas_en_mes(request):
    if request.method == 'POST':
        mes = request.data.get('mes', None)

        if mes:
            try:
                facturas = Invoice.objects.filter(invoice_date__month=mes)
                # Puedes serializar las facturas aquí si deseas enviar datos serializados como respuesta
                serializer = InvoiceSerializer(facturas, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Invoice.DoesNotExist:
                return Response({'error': 'No se encontraron facturas para el mes especificado.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'error': 'El parámetro de mes es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Método no permitido.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)