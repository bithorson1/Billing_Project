import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_invoice_email_async(purchase):
    subject = f"Invoice #{purchase.id}"
    recipient = purchase.customer_email

    html_content = render_to_string("billing/email_invoice.html", {
        "purchase": purchase
    })

    def _send():
        email = EmailMultiAlternatives(
            subject=subject,
            body="Your invoice is shown below.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient]
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=True)

    threading.Thread(target=_send, daemon=True).start()
