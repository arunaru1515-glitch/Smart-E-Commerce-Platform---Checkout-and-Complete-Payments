from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.database import Base, engine
from app.order_models import Order
from app.payment_models import Payment
from app.product_models import Product
from app.routes.checkout import router as checkout_router
from app.routes.webhook import router as webhook_router


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="Smart E-Commerce Platform",
    description="Checkout and Complete Payments API",
    version="1.0.0"
)


# Register API routers
app.include_router(checkout_router)
app.include_router(webhook_router)


# Payment success page
@app.get("/order/success", response_class=HTMLResponse)
def payment_success():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Payment Successful</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f5f5f5;
                text-align: center;
                padding-top: 100px;
            }

            .box {
                background: white;
                width: 450px;
                margin: auto;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            }

            h1 {
                color: green;
            }

            p {
                font-size: 18px;
            }
        </style>
    </head>

    <body>

        <div class="box">
            <h1>Payment Successful!</h1>

            <p>
                Your order has been placed successfully.
            </p>

            <p>
                Payment received and order updated.
            </p>
        </div>

    </body>
    </html>
    """