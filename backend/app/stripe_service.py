import os

import stripe
from dotenv import load_dotenv


load_dotenv()


STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")


def get_stripe():
    if not STRIPE_SECRET_KEY:
        raise ValueError(
            "STRIPE_SECRET_KEY is missing. "
            "Please add it to the .env file before making a Stripe payment."
        )

    stripe.api_key = STRIPE_SECRET_KEY

    return stripe


def create_payment_intent(
    amount: int,
    currency: str,
    order_id: int
):
    stripe_client = get_stripe()

    payment_intent = stripe_client.PaymentIntent.create(
        amount=amount,
        currency=currency,
        metadata={
            "order_id": str(order_id)
        }
    )

    return payment_intent


def create_checkout_session(
    amount: int,
    currency: str,
    order_id: int
):
    stripe_client = get_stripe()

    checkout_session = stripe_client.checkout.Session.create(
        mode="payment",

        line_items=[
            {
                "price_data": {
                    "currency": currency,
                    "product_data": {
                        "name": f"Order #{order_id}"
                    },
                    "unit_amount": amount
                },
                "quantity": 1
            }
        ],

        success_url=os.getenv(
            "FRONTEND_SUCCESS_URL",
            "http://localhost:3000/order/success"
        ),

        cancel_url=os.getenv(
            "FRONTEND_CANCEL_URL",
            "http://localhost:3000/order/cancel"
        ),

        metadata={
            "order_id": str(order_id)
        }
    )

    return checkout_session