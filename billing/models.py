from decimal import Decimal
from django.db import models


class Product(models.Model):
    product_code = models.CharField(max_length=30, unique=True, db_index=True)
    name = models.CharField(max_length=120)
    stock_available = models.PositiveIntegerField(default=0)

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        ordering = ("product_code",)

    def __str__(self):
        return f"{self.product_code} - {self.name}"


class Purchase(models.Model):
    customer_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_tax = models.DecimalField(max_digits=12, decimal_places=2)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2)
    rounded_amount = models.DecimalField(max_digits=12, decimal_places=2)

    cash_received = models.DecimalField(max_digits=12, decimal_places=2)
    balance_to_customer = models.DecimalField(max_digits=12, decimal_places=2)

    denomination_breakdown = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Purchase #{self.pk}"


class PurchaseLineItem(models.Model):
    purchase = models.ForeignKey(Purchase, related_name="line_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return f"{self.product.product_code} x {self.quantity}"
