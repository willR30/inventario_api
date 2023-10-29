from rest_framework import routers
from django.urls import path, include
from .views import PaymentTypeViewSet, CurrencyViewSet, PlanTypeViewSet, BusinessViewSet, UserRoleViewSet, SubUserRegistrationViewSet, ProductCategoryViewSet
from rest_framework.documentation import include_docs_urls
     

#this is a default crud api with django framework, this include the default UI
router = routers.DefaultRouter()
router.register(r'payment-types', PaymentTypeViewSet)
router.register(r'currencies', CurrencyViewSet)
router.register(r'plan-types', PlanTypeViewSet)
router.register(r'businesses', BusinessViewSet)
router.register(r'user-roles', UserRoleViewSet)
router.register(r'sub-user-registrations', SubUserRegistrationViewSet)

urlpatterns = [

    #ruta para documentacion
    path('docs/', include_docs_urls(title='API Documentation')),

    path('api/', include(router.urls)),

    path('user/', include('api.user.user_urls')),

    path('other/', include('api.others.other_urls')),

    path('products/', include('api.products.urls_products')),

    path('customers/', include('api.customers.customer_urls')),

    path('suppliers/', include('api.suppliers.supplier_urls')),

    path('products_category/', include('api.products_category.products_category_urls')),

    path('sale/', include('api.sale.sale_urls')),

    path('invoice/', include('api.invoice.invoice_urls')),   


]
