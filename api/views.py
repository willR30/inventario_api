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
    user = request.user  # Obtener el usuario autenticado
    business = Business.objects.get(user=user)
    return business


def decrement_register_available_for_business(request):
    business_id = get_business_id_by_user_from_server(request)
    try:
        business = Business.objects.get(id=business_id)
        business.last_registered_invoice -= 1
        business.save()
        return True  # Return True to indicate success
    except Business.DoesNotExist:
        return False  # Return False to indicate failure


def increment_register_available_for_business(request):
    business_id = get_business_id_by_user_from_server(request)
    try:
        business = Business.objects.get(id=business_id)
        business.last_registered_invoice += 1
        business.save()
        return True  # Return True to indicate success
    except Business.DoesNotExist:
        return False  # Return False to indicate failure


def get_csrf_token(request):
    _csrf_token = get_token(request)
    return JsonResponse({'csrf_token': _csrf_token})
