from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.db import models


# Modelo para PaymentType
class PaymentType(models.Model):
    '''
        Diferentes tipos de ejemplo: Efectivo, Transferencia, Bitcoin etc
    '''
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, null=True)


# Modelo para Currency
class Currency(models.Model):
    '''
        Nombre: Córdoba, Símbolo: C$, Identificador Internacional: NIO
    '''
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    international_identifier = models.CharField(max_length=10)


# Modelo para PlanType
class PlanType(models.Model):
    '''
        Se liminta una cantidad de registros por plan ejemplo:
        Free, 100 registros de productos maximos.
        Basic, 1000 registros de producto máximos.
    '''
    name = models.CharField(max_length=100)
    max_product_record_count = models.IntegerField()


# Modelo para Business
class Business(models.Model):
    '''
        La cuenta principal está vinculada con un negocio
        authorization_number,invocice_series e invoice_number son numeros brindadas con la DGI
        photo_link: url de la imagen alojada en el servidor
        Se vincula con el usuario creado en la tabla User
        Se relaciona con el tipo de plan escogido
        y La moneda por defecto en la que estará su sistema - esto no debe poder ser editado
    '''
    name = models.CharField(max_length=255)
    photo_link = models.TextField(null=True)
    authorization_number = models.CharField(max_length=100)
    invoice_series = models.CharField(max_length=50)
    invoice_number = models.CharField(max_length=10)
    last_registered_invoice = models.CharField(max_length=10)  # por defecto el valor al crear la cuenta es 0
    number_of_product_records_available = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_type = models.ForeignKey(PlanType, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)


# Modelo para UserRole
class UserRole(models.Model):
    '''
        estos roles están predefinidos dentro de la aplicacion
        Ejemplo: role cajejo, detail, solo tiene acceso a facturar
    '''
    role = models.CharField(max_length=50)
    detail = models.CharField(max_length=255, null=True)


# Modelo para SubUserRegistration
class SubUserRegistration(models.Model):
    '''
        Registro de sub usuarios que pertenecen a un mismo negocio
        se relaciona con un rol
    '''
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE)


# Modelo para ProductCategory
class ProductCategory(models.Model):
    '''
        Categoría de productos que se vinculan a un negocio
        name: Frutas
        icon_link: url de imagen dentro del server
        business: id del negocio que la está agregando
    '''
    name = models.CharField(max_length=100)
    icon_link = models.TextField(null=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)


# Modelo para Product
class Product(models.Model):
    '''
        Productos:
        photo_link: foto del producto, url dentro del server
        name: Manzana
        stock: 10
        cost_price:7
        sale_price: 10
        category: Frutas
        with_iva: true/false
    '''
    photo_link = models.TextField(null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    stock = models.IntegerField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    with_iva = models.BooleanField()  # en esta version todos los productos tienen iva


# Modelo para Supplier
class Supplier(models.Model):
    '''
        business: id del negocio que lo agregó
        s_address: dirección del proveedor
    '''
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    s_address = models.CharField(max_length=254)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)


# Modelo para Customer
class Customer(models.Model):
    '''
        c_address: dirección del cliente
        business: id del negocio que lo agregró
    '''
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    c_address = models.CharField(max_length=254)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)


# Modelo para Sale
class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cost_price_at_time = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price_at_time = models.DecimalField(max_digits=10, decimal_places=2)
    # invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)


# Modelo para Invoice
class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50)
    invoice_date = models.DateTimeField()
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    sale = models.ManyToManyField(Sale)
