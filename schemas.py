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