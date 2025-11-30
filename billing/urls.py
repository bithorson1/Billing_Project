from django.urls import path
from . import views

urlpatterns = [
    path("", views.billing_entry, name="billing_entry"),
    path("summary/<int:purchase_id>/", views.billing_summary, name="billing_summary"),
    path("history/", views.purchase_history, name="purchase_history"),
]
