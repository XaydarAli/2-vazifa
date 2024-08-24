from fastapi import APIRouter
from schemas import RegisterModel,LoginModel
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
    return users