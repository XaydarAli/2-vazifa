from http.client import HTTPException

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, status
from database import Session, ENGINE
from models import Product,Order,User
from schemas import ProductCreateModel,ProductUpdateModel

product_router = APIRouter(prefix="/products", tags=["Products"])
session = Session(bind=ENGINE)


@product_router.get("/")
async def products():
    products = session.query(Product).all()
    return products


@product_router.post("/")
async def product_create(product: ProductCreateModel):
    check_id = session.query(Product).filter(Product.id == product.id).scalar()
    if check_id is not None:
        return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Product id already exists")

    new_product = Product(
        id=product.id,
        name=product.name,
        price=product.price,

    )
    session.add(new_product)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="Product is created Successfully")




@product_router.get('/{id}')
async def product_detail(id: int):
    product = session.query(Product).filter(Product.id == id).first()
    if product is not None:
        context = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
        }
        return jsonable_encoder(context)

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product is not found")







@product_router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete(id: int):
    product = session.query(Product).filter(Product.id == id).first()
    if product:
        session.delete(product)
        session.commit()
        data = {
            "code": 200,
            "message": f"Product with  {id} is deleted successfully ",
        }
        return jsonable_encoder(data)

    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="this product is not found")


@product_router.put('/{id}')
async def update_product(id: int, data: ProductUpdateModel):
    product = session.query(Product).filter(Product.id == id).first()
    if product:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(product, key, value)
        session.commit()
        data = {
            "code": 200,
            "message": "PRODUCT IS UPDATED succesfully"
        }
        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="this product is not found")


@product_router.get("/product/{id}")
async def product_details(product_id: int):
    orders = session.query(Order).filter(Order.product_id == product_id).all()

    if not orders:
        return  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No orders found for this product")

    user_ids = {order.user_id for order in orders}

    users = session.query(User).filter(User.id.in_(user_ids)).all()

    users_data = [
        {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        for user in users
    ]

    return jsonable_encoder(users_data)