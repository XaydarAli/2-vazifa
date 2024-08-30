from http.client import HTTPException

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, status
from database import Session, ENGINE
from models import Order, User, Product
from schemas import OrderCreateModel,OrderListModel,OrderUpdateModel

order_router = APIRouter(prefix="/orders", tags=["Orders"])
session = Session(bind=ENGINE)


@order_router.get("/")
async def order_list():
    orders = session.query(Order).all()
    context = [
        {
            "id": order.id,
            "quantity": order.quantity,
            "user_id": order.user_id,
            "product_id": order.product_id,
            "cargo_id": order.cargo_id,
        }
        for order in orders
    ]
    return jsonable_encoder(context)


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




@order_router.get('/{id}')
async def order_detail(id: int):
    order = session.query(Order).filter(Order.id == id).first()
    if order is not None:
        context = {
            "id": order.id,
            "quantity": order.quantity,
            "user_id": order.user_id,
            "product_id": order.product_id,
            "cargo_id": order.cargo_id,
        }
        return jsonable_encoder(context)

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday order qilinmagan")




@order_router.put('/{id}')
async def update_order(id: int, data: OrderUpdateModel):
    order = session.query(Order).filter(Order.id == id).first()
    if order:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(order, key, value)
        session.commit()
        data = {
            "code": 200,
            "message": "Orderga o'zgaritirish kiritildi"
        }
        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bunday order qilinmagan")








@order_router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete(id: int):
    order = session.query(Order).filter(Order.id == id).first()
    if Order:
        session.delete(order)
        session.commit()
        data = {
            "code": 200,
            "message": f"{id} id lik order bekor qilindi ",
        }
        return jsonable_encoder(data)

    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday order qilinmagan")



@order_router.get("/user/{id}")
async def user_details(id:int):
    user=session.query(User).filter(User.id==id).first()
    if user:
        orders=session.query(Order).filter(Order.user_id==id).all()

        orders_data=[
            {
                'id':order.id,
                "product":order.product_id,
                "quantity":order.quantity
            }
            for order in orders
        ]
        data={
            "username":user.username,
            "email":user.email,
            "orders":orders_data
        }
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")