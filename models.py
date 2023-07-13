from database import Base
from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    
class Blog(Base):
    __tablename__ = "blogs"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    