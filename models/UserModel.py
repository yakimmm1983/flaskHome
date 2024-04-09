from pydantic import BaseModel


class UserModel(BaseModel):
    access_token:str
    login:str
    full_name:str
    id:int
