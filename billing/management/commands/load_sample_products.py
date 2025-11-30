from django.core.management.base import BaseCommand
from billing.models import Product


class Command(BaseCommand):
    help = "Load required sample products into the Product table"

    def handle(self, *args, **kwargs):
        sample_products = [
            {
                "product_code": "BOOK01",
                "name": "Books",
                "unit_price": 50,
                "tax_percentage": 5,
                "stock_available": 200
            },
            {
                "product_code": "PEN01",
                "name": "Pen",
                "unit_price": 10,
                "tax_percentage": 5,
                "stock_available": 500
            },
            {
                "product_code": "NOTE01",
                "name": "Notebook",
                "unit_price": 40,
                "tax_percentage": 8,
                "stock_available": 350
            },
            {
                "product_code": "BAG01",
                "name": "School Bag",
                "unit_price": 500,
                "tax_percentage": 12,
                "stock_available": 50
            }
        ]

        created_count = 0
        skipped_count = 0

        for item in sample_products:
            if not Product.objects.filter(product_code=item["product_code"]).exists():
                Product.objects.create(**item)
                created_count += 1
            else:
                skipped_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Loaded sample products successfully! Created: {created_count}, Skipped: {skipped_count}"
        ))
