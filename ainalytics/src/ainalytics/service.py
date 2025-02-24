from ainalytics.agent.flow import Flow
from ainalytics.agent.models import Chart
from ainalytics.database import PersistedFlowState, engine

from sqlmodel import Session, select

DATABASE_DESC = """
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

"""

charts = [
    Chart(
        name="pie",
        description="Used to show proportions or percentages of a whole, where each slice represents a category's contribution.",
    ),
    Chart(
        name="line",
        description="Ideal for displaying trends over time, showing continuous data points connected by lines.",
    ),
    Chart(
        name="bar",
        description="Effective for comparing quantities across different categories, using horizontal or vertical bars.",
    ),
]


def run_new_agent(message: str):
    flow = Flow(database_desc=DATABASE_DESC, chart_desc=charts)
    state = flow.run(message)

    with Session(engine) as session:
        obj = PersistedFlowState.from_flow_state(state)
        session.add(obj)
        session.commit()
        session.refresh(obj)

    data = [{"name": pt[0], "value": pt[1]} for pt in state.data]
    return state, data, obj.id


def run_agent(message: str, state_id: int):
    with Session(engine) as session:
        statement = select(PersistedFlowState).where(PersistedFlowState.id == state_id)
        obj = session.exec(statement).first()
        state = obj.to_flow_state()
    flow = Flow(database_desc=DATABASE_DESC, chart_desc=charts, state=state)
    state = flow.run(message)
    obj.update(state)
    with Session(engine) as session:
        session.add(obj)
        session.commit()

    data = [{"name": pt[0], "value": pt[1]} for pt in state.data]
    return state, data
