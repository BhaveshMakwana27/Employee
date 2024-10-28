from pydantic import BaseModel,EmailStr
from typing import Optional

class CreateEmployee(BaseModel):
    name:str
    email:EmailStr
    department:Optional[str] = None
    role:Optional[str] = None

class UpdateEmployee(BaseModel):
    name:Optional[str] = None
    email:Optional[EmailStr] = None
    department:Optional[str] = None
    role:Optional[str] = None


class TokenData(BaseModel):
    id:Optional[int] = None

class Token(BaseModel):
    access_token : str
    token_type : str