from pydantic import BaseModel
from fastapi import APIRouter, Depends ,Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.future import select
from sqlalchemy import insert, exists, delete
from jose import jwt
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
import os 
from models.model import Post,Comment,Likes
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db



fullPost = APIRouter()

template = Jinja2Templates(directory="templates")

class postData(BaseModel):
    post:str


@fullPost.get("/viewPost")
async def view_post(request:Request,post:str, db:AsyncSession=Depends(get_db)):
    add_pydantic = postData(post=post)

    db_comment = select(Comment).where(Comment.post==add_pydantic.post)
    result = await db.execute(db_comment)
    comment = result.scalars().all()

    get_db = select(Post).where(Post.id==add_pydantic.post)
    result = await db.execute(get_db)
    post =  result.scalar_one_or_none()
    likes = await db.execute(select(Likes))

    result_like= likes.scalars().all()

    return template.TemplateResponse("post.html" ,{"request":request, "post":post, "comments":comment, "likes":result_like} )