from pydantic import BaseModel

class User(BaseModel):
    username : str
    password : str
    email : str
    
class Blog(BaseModel):
    title : str
    body : str