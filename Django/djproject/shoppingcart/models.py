from django.db import models
# Create your models here.
#from phonenumber_field.modelfields import PhoneNumberField

class Cateogary(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    cateogary = models.ForeignKey(Cateogary , on_delete = models.CASCADE, default=0)
    image = models.ImageField(upload_to = "pics")
    purchase_price = models.IntegerField()
    sale_price = models.IntegerField()
    stock_available = models.IntegerField()
    sku = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SalesOrder(models.Model):
    date = models.DateField(max_length=50)
    user_id = models.CharField(max_length=50)

class SaleOrderItem(models.Model):
    product_id = models.ForeignKey(Product,  on_delete=models.CASCADE, default=0)
    order_id = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, default=0)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class User(models.Model):
    user_name = models.CharField(max_length=50, default=0)
    password = models.CharField(max_length=50, default=0)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    def __str__(self):
        return self.user_name

class Address(models.Model):
    country = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    post_code = models.CharField(max_length=100)

class Profile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    billing_address = models.ForeignKey(Address, related_name='billing_address', on_delete=models.CASCADE, default=0)
    shipping_address = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.CASCADE, default=0)