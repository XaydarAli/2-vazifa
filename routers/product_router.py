from http.client import HTTPException
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, status
from database import Session, ENGINE
from models import Product
from schemas import ProductCreateModel

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




