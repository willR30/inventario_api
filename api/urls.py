from rest_framework import routers
from django.urls import path, include
from .views import PaymentTypeViewSet, CurrencyViewSet, PlanTypeViewSet, BusinessViewSet, UserRoleViewSet, SubUserRegistrationViewSet, ProductCategoryViewSet, ProductViewSet, SupplierViewSet, CustomerViewSet, InvoiceViewSet, SaleViewSet
from rest_framework import views as drf_views
from .views import register_user, user_login, user_logout, restar_stock,facturas_de_cliente, facturas_en_rango, facturas_en_mes
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'payment-types', PaymentTypeViewSet)
router.register(r'currencies', CurrencyViewSet)
router.register(r'plan-types', PlanTypeViewSet)
router.register(r'businesses', BusinessViewSet)
router.register(r'user-roles', UserRoleViewSet)
router.register(r'sub-user-registrations', SubUserRegistrationViewSet)
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'sales', SaleViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('user/register/', register_user, name='register'),
    path('user/login/', user_login, name='login'),
    path('user/logout/', user_logout, name='logout'),
    # Otras rutas
    path('others/restar-stock/',restar_stock, name='restar-stock'),
    path('others/facturas-de-cliente/',facturas_de_cliente, name='facturas-de-cliente'),
    path('others/facturas-en-rango/', facturas_en_rango, name='facturas-en-rango'),
    path('others/facturas-en-mes/', facturas_en_mes, name='facturas-en-mes'),
]
