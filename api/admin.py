from django.contrib import admin
from .models import PaymentType, Currency, PlanType, Business, UserRole, SubUserRegistration, ProductCategory, Product, Supplier, Customer, Invoice, Sale

# Register your models here
admin.site.register(PaymentType)
admin.site.register(Currency)
admin.site.register(PlanType)
admin.site.register(Business)
admin.site.register(UserRole)
admin.site.register(SubUserRegistration)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(Invoice)
admin.site.register(Sale)
