from django.contrib import admin
from billing.models import *

admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(PurchaseLineItem)
