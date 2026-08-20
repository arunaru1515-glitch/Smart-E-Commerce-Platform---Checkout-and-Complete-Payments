from app.database import Base, SessionLocal, engine
from app.product_models import Product


# Create products table if it does not exist
Base.metadata.create_all(bind=engine)


db = SessionLocal()

try:
    products = [
        Product(
            name="Laptop",
            description="High performance laptop",
            price=75000,
            category="Electronics",
            popularity=95,
            stock_quantity=10,
            is_available=True
        ),
        Product(
            name="Smartphone",
            description="Latest generation smartphone",
            price=45000,
            category="Electronics",
            popularity=92,
            stock_quantity=18,
            is_available=True
        ),
        Product(
            name="Wireless Headphones",
            description="Noise cancelling wireless headphones",
            price=5000,
            category="Electronics",
            popularity=88,
            stock_quantity=25,
            is_available=True
        )
    ]

    db.add_all(products)
    db.commit()

    print("3 products inserted successfully.")

except Exception as e:
    db.rollback()
    print("Error inserting products:", e)

finally:
    db.close()