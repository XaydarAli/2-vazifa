from pydantic import BaseModel
from typing import List,Optional

class RegisterModel(BaseModel):
    id:Optional[int]
    username:Optional[str]
    email:Optional[str]
    password:Optional[str]
    is_active:Optional[bool]
    is_staff:Optional[bool]


    class Config:
        orm_mode=True
        schema_extra={
            "id":1,
            "username":"whitewolf",
            "email":"khaydarovalijon1308@gmail.com",
            "password":"Alijon1308",
            "is_active":True,
            "is_staff":True,
        }


class LoginModel(BaseModel):
    username:Optional[str]
    password:Optional[str]




class UserListModel(BaseModel):
    id: Optional[int]
    username:Optional[str]
    first_name:Optional[str]
    last_name:Optional[str]
    password:Optional[str]




# class UserCreateModel(BaseModel):
#     id: Optional[int]
#     username:Optional[str]
#     first_name:Optional[str]
#     last_name:Optional[str]
#     password:Optional[str]
#

class UserUpdateModel(BaseModel):
    id: Optional[int]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]



class ProductModel(BaseModel):
    id: Optional[int]
    name: Optional[str]
    price: Optional[float]

    class Config:
        orm_mode = True
        schema_extra = {
            'id': 1,
            'name':'example_product',
            'price':1,

        }












class ProductCreateModel(BaseModel):
    id: Optional[int]
    name: Optional[str]
    price: Optional[int]


class ProductListModel(BaseModel):
    id: Optional[int]
    name: Optional[str]
    price: Optional[int]


class ProductUpdateModel(BaseModel):
    id: Optional[int]
    name: Optional[str]
    price: Optional[int]


class OrderListModel(BaseModel):
    id: Optional[int]
    quantity: Optional[int]
    user_id: Optional[str]
    product_id: Optional[int]
    cargo_id: Optional[int]


class OrderUpdateModel(BaseModel):
    id: Optional[int]
    quantity: Optional[int]
    user_id: Optional[str]
    product_id: Optional[int]
    cargo_id: Optional[int]


class OrderCreateModel(BaseModel):
    id: Optional[int]
    quantity: Optional[int]
    user_id: Optional[int]
    product_id: Optional[int]












class CargoModel(BaseModel):
    id: Optional[int]
    shipping_address: Optional[str]
    tracking_number: Optional[str]
    class Config:
        orm_mode = True
        schema_extra = {
            'id': 1,
            'shipping_address': None,
            'tracking_number': None,
        }