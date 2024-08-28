from fastapi import FastAPI
from routers.auth_router import auth_router
from routers.order_router import order_router
from routers.product_router import product_router
from routers.cargo_router import  cargo_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(order_router)
app.include_router(product_router)
app.include_router(cargo_router)
@app.get("/")
async def root():
    return {"message": "Siz home pagedasiz"}