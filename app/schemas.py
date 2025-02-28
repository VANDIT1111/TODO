from pydantic import BaseModel
from enum import Enum


class RoleEnum(str,Enum):
    ADMIN = 'admin'
    USER = 'user'
    
    
class TaskStatusEnum(str,Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    

class UserCreate(BaseModel):
    username:str
    email:str
    password:str
    role:RoleEnum
    
class UserOut(BaseModel):
    username:str
    email:str
    role:RoleEnum
    
class UserLogin(BaseModel):
    username:str
    email:str
    password:str
    
class UserResponse(BaseModel):
    id:int
    
    class config:
        orm_mode=True
    
class TaskBase(BaseModel):
    id:int
            


class TaskCreate(BaseModel):
    title:str
    description:str
    
class TaskUpdate(BaseModel):
    title:str
    description:str
    status:TaskStatusEnum
    
class TaskDelete(BaseModel):
    pass
    
class TaskView(BaseModel):
    pass
    

class TaskOut(BaseModel):
    id:int
    owner_id:int

    class config:
        orm_mode=True
    
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None