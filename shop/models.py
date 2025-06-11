from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal, ROUND_HALF_UP

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.brand.name})"

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def discounted_price(self):
        discounted = self.product.selling_price - self.discount
        return max(Decimal('0.00'), discounted).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def total_price(self):
        return (self.discounted_price() * self.quantity).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

class Sale(models.Model):
    date = models.DateTimeField(auto_now_add=True)

    def total_amount(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Sale #{self.id} - {self.date.strftime('%d %b %Y %H:%M')}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    discount = models.FloatField(default=0.0)  # in percentage

    def discounted_price(self):
        selling_price = self.product.selling_price
        discount_decimal = Decimal(str(self.discount)) / Decimal('100')
        discounted = selling_price * (Decimal('1') - discount_decimal)
        return discounted.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def total_price(self):
        return (self.discounted_price() * self.quantity).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    discount = models.FloatField(default=0.0)  # in percentage

    @property
    def discounted_price(self):
        selling_price = self.product.selling_price
        discount_decimal = Decimal(str(self.discount)) / Decimal('100')
        discounted = selling_price * (Decimal('1') - discount_decimal)
        return discounted.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def total_price(self):
        return (self.discounted_price * self.quantity).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
