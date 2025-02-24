from typing import List, Optional
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship, create_engine, Session
from sqlalchemy.sql.expression import text

from ainalytics.config import settings


# Customers Table
class Customers(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    orders: List["Orders"] = Relationship(back_populates="customers")


# Products Table
class Products(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    category_id: Optional[int] = Field(default=None, foreign_key="categories.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    category: Optional["Categories"] = Relationship(back_populates="products")
    order_items: List["OrderItems"] = Relationship(back_populates="product")


# Categories Table
class Categories(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: str

    products: List["Products"] = Relationship(back_populates="category")


# Orders Table
class Orders(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customers.id")
    order_date: datetime = Field(default_factory=datetime.now)
    total_amount: float
    status: str  # e.g., "Pending", "Shipped", "Delivered", "Cancelled"

    customers: Customers = Relationship(back_populates="orders")
    order_items: List["OrderItems"] = Relationship(back_populates="order")


# OrderItems Table
class OrderItems(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    product_id: int = Field(foreign_key="products.id")
    quantity: int
    price_at_time_of_purchase: float

    order: Orders = Relationship(back_populates="order_items")
    product: Products = Relationship(back_populates="order_items")


engine = create_engine(settings.DATABASE_URL)


def exec_sql(statement: str):
    with Session(engine) as session:
        result = session.exec(text(statement))
        return result


# Create all tables
def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables(engine)
