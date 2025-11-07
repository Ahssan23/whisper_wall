from fastapi import APIRouter, Depends, Request, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.future import select
from sqlalchemy import insert, exists, delete
from jose import jwt
from dotenv import load_dotenv
import os 
from models.model import Comment
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db

load_dotenv()


comment = APIRouter()

template = Jinja2Templates(directory="templates")


class commentPost(BaseModel):
    comment:str
    username:str
    post:str


class PostId(BaseModel):
    post:str


@comment.get("/comments")
async def get_comments(request:Request,post:str, db:AsyncSession=Depends(get_db)):
    add_pydantic = PostId(post=post)

    db_comment = select(Comment).where(Comment.post==add_pydantic.post)
    result = await db.execute(db_comment)
    comment = result.scalars().all()
    

    return template.TemplateResponse("template.html" , {"request":request, "comments":comment})


        



@comment.post("/comment" , response_class=HTMLResponse)
async def comment_post(request:Request, comment_text:str=Form(...) ,post_id:str=Form(...), token:str=Cookie(None) ,db:AsyncSession=Depends(get_db)):
    try:
        ALGORITHM = 'HS256'
        decoded = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=[ALGORITHM])

        add_comment = commentPost(username=decoded['username'], post=post_id, comment=comment_text)
        add_db = Comment(**add_comment.model_dump())

        db.add(add_db)
        await db.commit()
        await db.refresh(add_db)
        referer = request.headers.get("referer")

        return RedirectResponse(url=referer, status_code=302)
    

    except Exception as error:
        print(error)
        return RedirectResponse(url="/login", status_code=302)