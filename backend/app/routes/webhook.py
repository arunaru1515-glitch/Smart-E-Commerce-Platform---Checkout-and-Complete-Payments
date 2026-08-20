import os
import stripe

from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.database import get_db
from app.order_models import Order
from app.payment_models import Payment


load_dotenv()

stripe_webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")


router = APIRouter(
    prefix="/webhook",
    tags=["Webhook"]
)


@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    payload = await request.body()
    signature = request.headers.get("stripe-signature")

    # Validate Stripe webhook
    try:
        event = stripe.Webhook.construct_event(
            payload,
            signature,
            stripe_webhook_secret
        )

    except Exception as e:
        print("WEBHOOK ERROR:", str(e))

        raise HTTPException(
            status_code=400,
            detail="Invalid Stripe webhook"
        )

    event_type = event["type"]

    print("WEBHOOK EVENT:", event_type)

    # --------------------------------
    # PAYMENT SUCCESS
    # --------------------------------
    if event_type in [
        "checkout.session.completed",
        "payment_intent.succeeded"
    ]:

        data = event["data"]["object"].to_dict()

        order_id = data.get("metadata", {}).get("order_id")

        print("ORDER ID FROM STRIPE:", order_id)

        if order_id:

            order = db.query(Order).filter(
                Order.id == int(order_id)
            ).first()

            payment = db.query(Payment).filter(
                Payment.order_id == int(order_id)
            ).first()

            # Update Order
            if order:
                order.payment_status = "paid"
                order.order_status = "paid"

                print(
                    "ORDER UPDATED:",
                    order.id,
                    "-> PAID"
                )

            # Update Payment
            if payment:
                payment.status = "succeeded"

                print(
                    "PAYMENT UPDATED:",
                    payment.id,
                    "-> SUCCEEDED"
                )

            db.commit()

    # --------------------------------
    # PAYMENT FAILED
    # --------------------------------
    elif event_type == "payment_intent.payment_failed":

        payment_intent = event["data"]["object"].to_dict()

        order_id = payment_intent.get(
            "metadata",
            {}
        ).get("order_id")

        print("ORDER ID FROM STRIPE:", order_id)

        if order_id:

            order = db.query(Order).filter(
                Order.id == int(order_id)
            ).first()

            payment = db.query(Payment).filter(
                Payment.order_id == int(order_id)
            ).first()

            # Update Order
            if order:
                order.payment_status = "failed"

                print(
                    "ORDER UPDATED:",
                    order.id,
                    "-> FAILED"
                )

            # Update Payment
            if payment:
                payment.status = "failed"

                print(
                    "PAYMENT UPDATED:",
                    payment.id,
                    "-> FAILED"
                )

            db.commit()

    # --------------------------------
    # OTHER STRIPE EVENTS
    # --------------------------------
    else:
        print(
            "EVENT IGNORED:",
            event_type
        )

    return {
        "message": "Webhook received successfully",
        "event_type": event_type
    }