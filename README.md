# Smart E-Commerce Platform – Checkout and Complete Payments

## Project Overview

This project implements a complete checkout and payment system for a Smart E-Commerce Platform using FastAPI, SQLAlchemy, MySQL, and Stripe.

The system validates cart items, calculates the total order amount, creates orders, processes payments through Stripe, handles Stripe webhooks, and automatically updates order and payment statuses in the database.

## Features

- Product and stock validation
- Cart quantity validation
- Automatic total price calculation
- Order creation and management
- Stripe Payment Intent integration
- Stripe Checkout Session integration
- Stripe webhook integration
- Payment transaction tracking
- Automatic order status updates
- Automatic payment status updates
- MySQL database integration
- Payment success page
- Swagger API documentation

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- MySQL
- Stripe
- Pydantic
- Uvicorn
- python-dotenv

## Checkout and Payment Flow

1. User submits the cart for checkout.
2. Products are validated against the database.
3. Product availability and stock are checked.
4. The total order amount is calculated.
5. A new order is created with a pending payment status.
6. A Stripe Payment Intent is created.
7. A Stripe Checkout Session is created.
8. The user completes the payment through Stripe.
9. Stripe sends payment events through the webhook.
10. The webhook updates the order and payment status in MySQL.
11. The successful payment is reflected in the application.

## API Endpoints

### Checkout

```text
POST /checkout
