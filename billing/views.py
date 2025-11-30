from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.urls import reverse

from .forms import BillingForm, ProductLineFormSet, DenominationForm
from .utils import calculate_denomination_breakdown
from .utils_email import send_invoice_email_async
from .models import Product, Purchase, PurchaseLineItem


def billing_entry(request):

    if request.method == "POST":
        billing_form = BillingForm(request.POST)
        line_formset = ProductLineFormSet(request.POST)
        denom_form = DenominationForm(request.POST)

        if billing_form.is_valid() and line_formset.is_valid() and denom_form.is_valid():

            customer_email = billing_form.cleaned_data["customer_email"]
            cash_received = billing_form.cleaned_data["cash_received"]

            total_price = Decimal("0")
            total_tax = Decimal("0")
            line_items_buffer = []

            for form in line_formset:
                if not form.cleaned_data or form.cleaned_data.get("DELETE"):
                    continue

                product = form.cleaned_data["product"]
                qty = form.cleaned_data["quantity"]

                subtotal = product.unit_price * qty
                tax_amount = subtotal * (product.tax_percentage / Decimal("100"))
                total_amount = subtotal + tax_amount

                total_price += subtotal
                total_tax += tax_amount

                line_items_buffer.append({
                    "product": product,
                    "quantity": qty,
                    "unit_price": product.unit_price,
                    "tax_percentage": product.tax_percentage,
                    "subtotal": subtotal,
                    "tax_amount": tax_amount,
                    "total_amount": total_amount,
                })

            if not line_items_buffer:
                billing_form.add_error(None, "Please add at least one valid product.")
            else:
                net_amount = total_price + total_tax
                rounded_amount = Decimal(round(net_amount))
                balance = cash_received - rounded_amount

                shop_notes = {
                    500: denom_form.cleaned_data["d500"],
                    50: denom_form.cleaned_data["d50"],
                    20: denom_form.cleaned_data["d20"],
                    10: denom_form.cleaned_data["d10"],
                    5: denom_form.cleaned_data["d5"],
                    2: denom_form.cleaned_data["d2"],
                    1: denom_form.cleaned_data["d1"],
                }

                change_breakdown = calculate_denomination_breakdown(balance, shop_notes)

                with transaction.atomic():
                    purchase = Purchase.objects.create(
                        customer_email=customer_email,
                        total_price=total_price,
                        total_tax=total_tax,
                        net_amount=net_amount,
                        rounded_amount=rounded_amount,
                        cash_received=cash_received,
                        balance_to_customer=balance,
                        denomination_breakdown=change_breakdown,
                    )

                    for item in line_items_buffer:
                        PurchaseLineItem.objects.create(
                            purchase=purchase,
                            product=item["product"],
                            quantity=item["quantity"],
                            unit_price=item["unit_price"],
                            tax_percentage=item["tax_percentage"],
                            subtotal=item["subtotal"],
                            tax_amount=item["tax_amount"],
                            total_amount=item["total_amount"],
                        )

                send_invoice_email_async(purchase)

                return redirect(reverse("billing_summary", args=[purchase.id]))

    else:
        billing_form = BillingForm()
        line_formset = ProductLineFormSet()
        denom_form = DenominationForm()

    return render(request, "billing/billing_form.html", {
        "billing_form": billing_form,
        "line_formset": line_formset,
        "denomination_form": denom_form,
    })


def billing_summary(request, purchase_id):
    purchase = get_object_or_404(Purchase, pk=purchase_id)

    return render(request, "billing/billing_summary.html", {
        "purchase": purchase,
        "change": purchase.denomination_breakdown
    })


def purchase_history(request):
    email = request.GET.get("email")
    purchases = Purchase.objects.filter(customer_email=email) if email else []

    return render(request, "billing/purchase_history.html", {
        "email": email,
        "purchases": purchases
    })
