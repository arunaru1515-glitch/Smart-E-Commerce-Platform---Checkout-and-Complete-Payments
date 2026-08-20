from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, Integer, JSON, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    products: Mapped[list] = mapped_column(
        JSON,
        nullable=False
    )

    total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    payment_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending"
    )

    order_status: Mapped[str] = mapped_column(
        Enum(
            "pending",
            "paid",
            "shipped",
            "delivered",
            "cancelled",
            name="order_status"
        ),
        nullable=False,
        default="pending"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )