# Billing Project - Django Mini Task

## Overview
This project implements a complete billing system as required in the Python Mini Task PDF.  
It includes product selection, tax calculation, net amount calculation, rounding, balance return,
denomination breakdown, purchase history, and email invoice sending (asynchronously).

---

## Features Implemented

### ✔ Product Management
- Product model includes:
  - Product code
  - Product name
  - Unit price
  - Tax percentage  
- Loaded via Django admin.
- Dropdown product selector in billing page.

### ✔ Billing Page
- Customer email input
- Cash received from customer
- Add multiple product lines dynamically
- Select product + enter quantity
- Add/remove product rows
- Enter shop available denominations (500,50,20,10,5,2,1)

### ✔ Billing Calculations
- Price × quantity
- Tax calculation
- Net amount: `subtotal + tax`
- Rounded amount
- Balance return: `cash_received - rounded_amount`
- Denomination breakdown returned to customer

### ✔ Async Email Invoice
- Professional HTML invoice
- Sent in background using Python threading
- Gmail SMTP supported

### ✔ Purchase Summary Page
- Table of purchased items
- Totals and denomination breakdown

### ✔ Purchase History
- Search purchases by email
- View all previous bills

---


## Management Command (Important)

To load sample product data, run:

```
python manage.py load_sample_products
```

This will insert all required products into the database.
 
---

## Installation

### 1. Create virtual environment
```
python -m venv venv
venv\Scripts\activate   # Windows
```

### 2. Install libraries
```
pip install -r requirements.txt
```

### 3. Run migrations
```
python manage.py migrate
```

### 4. Load sample products (optional)
```
python manage.py load_sample_products
```

### 5. Run server
```
python manage.py runserver
```

---

## Email Configuration (Gmail)

Add this to `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'yourgmail@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password_without_spaces'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

Note: App password must be generated from Google Account → Security → App Passwords.

---

## Folder Structure

```
billing_project/
 ├── billing/
 │    ├── templates/
 │    │     ├── billing_form.html
 │    │     ├── billing_summary.html
 │    │     ├── purchase_history.html
 │    │     └── email_invoice.html
 │    ├── management/
 │    │     └── commands/
 │    │            └── load_sample_products.py
 │    ├── models.py
 │    ├── views.py
 │    ├── forms.py
 │    ├── utils.py
 │    └── utils_email.py
 ├── billing_project/
 ├── requirements.txt
 └── README.md
```

---

## Author
Task completed by Bithorson.S

