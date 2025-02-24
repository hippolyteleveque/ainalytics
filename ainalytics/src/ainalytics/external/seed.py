from sqlmodel import Session, select
from faker import Faker
from datetime import datetime, timedelta
import random


# Import your models and engine
from ainalytics.external.database import (
    Customers,
    Products,
    Categories,
    Orders,
    OrderItems,
    engine,
)

# Initialize Faker
fake = Faker()


# Helper function to generate a random date within the last year
def random_date():
    return datetime.now() - timedelta(days=random.randint(1, 365))


# Seed Customers
def seed_customers(session):
    for _ in range(50):  # Create 50 customers
        customers = Customers(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            created_at=random_date(),
            updated_at=random_date(),
        )
        session.add(customers)
    session.commit()


# Seed Categories
def seed_categories(session):
    categories = ["Electronics", "Clothing", "Home & Kitchen", "Books", "Toys"]
    for category_name in categories:
        category = Categories(
            name=category_name,
            description=fake.sentence(),
        )
        session.add(category)
    session.commit()


# Seed Products
def seed_products(session):
    categories = session.exec(select(Categories)).all()
    for _ in range(100):  # Create 100 products
        product = Products(
            name=fake.catch_phrase(),
            description=fake.text(),
            price=round(random.uniform(10, 1000), 2),
            category_id=random.choice(categories).id,
            created_at=random_date(),
            updated_at=random_date(),
        )
        session.add(product)
    session.commit()


# Seed Orders
def seed_orders(session):
    customers = session.exec(select(Customers)).all()
    for _ in range(200):  # Create 200 orders
        order = Orders(
            customer_id=random.choice(customers).id,
            order_date=random_date(),
            total_amount=round(random.uniform(50, 1000), 2),
            status=random.choice(["Pending", "Shipped", "Delivered", "Cancelled"]),
        )
        session.add(order)
    session.commit()


# Seed OrderItems
def seed_order_items(session):
    orders = session.exec(select(Orders)).all()
    products = session.exec(select(Products)).all()
    for order in orders:
        for _ in range(random.randint(1, 5)):  # Add 1-5 items per order
            product = random.choice(products)
            order_item = OrderItems(
                order_id=order.id,
                product_id=product.id,
                quantity=random.randint(1, 10),
                price_at_time_of_purchase=product.price,
            )
            session.add(order_item)
    session.commit()


# Main function to seed all tables
def seed_database():
    with Session(engine) as session:
        seed_customers(session)
        seed_categories(session)
        seed_products(session)
        seed_orders(session)
        seed_order_items(session)




# Run the seeding script
if __name__ == "__main__":
    seed_database()
    print("Database seeded successfully!")
