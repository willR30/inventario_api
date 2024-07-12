from rest_framework import viewsets, permissions
from django.middleware.csrf import get_token
from django.http import JsonResponse

from .models import PaymentType, Currency, PlanType, Business, UserRole, SubUserRegistration, ProductCategory, Product, \
    Supplier, Customer, Invoice, Sale
from .serializers import PaymentTypeSerializer, CurrencySerializer, PlanTypeSerializer, BusinessSerializer, \
    UserRoleSerializer, SubUserRegistrationSerializer, ProductCategorySerializer, ProductSerializer, SupplierSerializer, \
    CustomerSerializer, InvoiceSerializer, SaleSerializer


class PaymentTypeViewSet(viewsets.ModelViewSet):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class PlanTypeViewSet(viewsets.ModelViewSet):
    queryset = PlanType.objects.all()
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


def get_business_id_by_user_from_server(request):
    user = request.user
    try:
        # Asumiendo que cada usuario tiene un solo negocio
        business = Business.objects.get(user=user)
        return business.id
    except Business.DoesNotExist:
        return None



def decrement_register_available_for_business(request):
    business_id = get_business_id_by_user_from_server(request)
    try:
        # Obtener el objeto Business usando el ID
        business = Business.objects.get(id=business_id)
        # Decrementar el número de registros de productos disponibles
        business.number_of_product_records_available -= 1
        # Guardar el objeto Business actualizado
        business.save()
        return True  # Indicar éxito
    except Business.DoesNotExist:
        return False  # Indicar fracaso si no se encuentra el Business


def increment_register_available_for_business(request):
    business_id = get_business_id_by_user_from_server(request)
    try:
        business = Business.objects.get(id=business_id)
        business.number_of_product_records_available += 1
        business.save()
        return True  # Indicar éxito
    except Business.DoesNotExist:
        return False  # Indicar fracaso si no se encuentra el Business



def increment_last_registered_invoice(request):
    try:
        business = get_business_id_by_user_from_server(request)
        business.last_registered_invoice += 1
        business.save()
        return True  # Return True to indicate success
    except Business.DoesNotExist:
        return False  # Return False to indicate failure


def decrement_last_registered_invoice(request):
    try:
        business = get_business_id_by_user_from_server(request)
        business.last_registered_invoice -= 1
        business.save()
        return True  # Return True to indicate success
    except Business.DoesNotExist:
        return False  # Return False to indicate failure


