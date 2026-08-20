from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.order_models import Order
from app.payment_models import Payment
from app.product_models import Product
from app.stripe_service import (
    create_checkout_session,
    create_payment_intent,
)


class CartItem(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class CheckoutRequest(BaseModel):
    user: str
    products: list[CartItem] = Field(min_length=1)


router = APIRouter(
    prefix="/checkout",
    tags=["Checkout"]
)


@router.post("")
def checkout(
    request: CheckoutRequest,
    db: Session = Depends(get_db)
):
    total_price = Decimal("0.00")
    order_products = []

    # Validate cart items and calculate total
    for item in request.products:

        # Find product in MySQL
        product = db.get(Product, item.product_id)

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found"
            )

        # Check product availability
        if not product.is_available:
            raise HTTPException(
                status_code=400,
                detail=f"Product '{product.name}' is not available"
            )

        # Check stock
        if item.quantity > product.stock_quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for '{product.name}'"
            )

        # Calculate price using database price
        item_total = product.price * item.quantity
        total_price += item_total

        # Store product details in order
        order_products.append(
            {
                "product_id": product.id,
                "name": product.name,
                "quantity": item.quantity,
                "unit_price": str(product.price),
            }
        )

    # Create Order
    order = Order(
        user=request.user,
        products=order_products,
        total=total_price,
        payment_status="pending",
        order_status="pending"
    )

    # Save Order
    db.add(order)
    db.commit()
    db.refresh(order)

    # Convert INR to smallest currency unit
    amount = int(total_price * 100)

    # Create Stripe Payment Intent
    payment_intent = create_payment_intent(
        amount=amount,
        currency="inr",
        order_id=order.id
    )

    # Create Stripe Checkout Session
    checkout_session = create_checkout_session(
        amount=amount,
        currency="inr",
        order_id=order.id
    )

    # Create Payment record
    payment = Payment(
        order_id=order.id,
        amount=total_price,
        payment_method="stripe",
        transaction_id=payment_intent.id,
        status="pending"
    )

    # Save Payment
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "message": "Checkout created successfully",
        "order_id": order.id,
        "total": order.total,
        "payment_status": order.payment_status,
        "order_status": order.order_status,
        "payment_id": payment.id,
        "payment_method": payment.payment_method,
        "transaction_id": payment.transaction_id,
        "payment_intent_id": payment_intent.id,
        "checkout_session_id": checkout_session.id,
        "checkout_url": checkout_session.url
    }