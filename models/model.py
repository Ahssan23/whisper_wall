from sqlalchemy import Column, Integer, String
from db.db import Base




class User(Base):
    __tablename__ = "users"

    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100), unique=True, index=True)



class Post(Base):
    __tablename__ = "post"

    id = Column(Integer,primary_key=True, index=True)
    username = Column(String(50))
    title = Column(String(10))
    content = Column(String(1000))
    likes = Column(Integer)
    

class Likes(Base):
    __tablename__ = "likes"

    id = Column(Integer,primary_key=True, index=True)
    username = Column(String(50))
    post= Column(Integer)


class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, index=True)
    post = Column(Integer)
    username = Column(String(30))
    comment = Column(String(500))
    