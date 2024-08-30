from http.client import HTTPException

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql.functions import user
from starlette import status

from schemas import RegisterModel,LoginModel,UserUpdateModel
from database import Session,ENGINE
from models import User
from werkzeug.security import generate_password_hash,check_password_hash
auth_router = APIRouter(prefix="/auth", tags=["auth"])
session=Session(bind=ENGINE)

@auth_router.get("/")
async def auth():
    return {"message": "Auth page"}


@auth_router.get("/login")
async def login():
    return {"message": "Login page"}


@auth_router.post("/login")
async def user_login(user: LoginModel):
    check_user = session.query(User).filter(User.username == user.username).first()
    if check_user is not None:
        if check_password_hash(check_user.password, user.password):
            return {"message": "Login successful"}
        return {"message": "Incorrect  password"}
    return {"message": "User not found"}



@auth_router.get("/register")
async def get_register():
    return {"message": "Register page"}

@auth_router.post("/register")
async def create_user(user:RegisterModel):
    check_username=session.query(User).filter(User.username==user.username).first()
    if check_username is not None:
        return {"message": "User already exists"}
    check_email=session.query(User).filter(User.email==user.email).first()
    if check_email is not None:
        return {"message": "Email already exists"}
    new_user=User(
        id=user.id,
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,

    )
    session.add(new_user)
    session.commit()
    return {"message": "User created"}


@auth_router.get("/users")
async def get_users():
    users=session.query(User).all()
    data=[
        {   'id':user.id,
            'username':user.username,
            'email':user.email,
            'password':user.password,
        }
        for user in users
    ]
    return jsonable_encoder(data)






@auth_router.get('/{id}')
async def user_detail(id: int):
    user = session.query(User).filter(User.id == id).first()
    if user is not None:
        context = {
            "id": user.id,
            "username": user.username,
            "last_name": user.last_name,
            "first_name": user.first_name,
            "password":user.password,
        }
        return jsonable_encoder(context)

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bunday user yo'q")




@auth_router.put('/{id}')
async def update_user(id: int, data: UserUpdateModel):
    user = session.query(User).filter(User.id == id).first()
    if user:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(user, key, value)
        session.commit()
        data = {
            "code": 200,
            "message": "Userga o'zgaritirish kiritildi"
        }
        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bunday order qilinmagan")








@auth_router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete(id: int):
    user = session.query(User).filter(User.id == id).first()
    if User:
        session.delete(user)
        session.commit()
        data = {
            "code": 200,
            "message": f"{id} id lik user is deleted",
        }
        return jsonable_encoder(data)

    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday user mavjud emas")



