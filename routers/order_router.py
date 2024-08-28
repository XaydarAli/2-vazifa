from http.client import HTTPException
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, status
from database import Session, ENGINE
from models import Order, User, Product
from schemas import OrderCreateModel

order_router = APIRouter(prefix="/orders", tags=["Orders"])
session = Session(bind=ENGINE)


@order_router.get("/orders")
async def get_orders():
    orders = session.query(Order).all()
    return orders


@order_router.post("/")
async def create_order(order: OrderCreateModel):
    check_order = session.query(Order).filter(Order.id == order.id).first()
    if check_order is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order already exists")

    user_check = session.query(User).filter(User.id == order.user_id).first()
    if user_check is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User id not already exists")

    product_check = session.query(Product).filter(Product.id == order.product_id).first()
    if product_check is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product id already exists")

    new_order = Order(
        id=order.id,
        quantity=order.quantity,
        user_id=order.user_id,
        product_id=order.product_id,
    )
    session.add(new_order)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Ordered successfully")