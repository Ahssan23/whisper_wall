from fastapi import APIRouter,Depends, Form, Request,Response,Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.future import select
from sqlalchemy import insert, exists, delete
from jose import jwt
from dotenv import load_dotenv
import os 
from models.model import Likes
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from db.db import get_db

load_dotenv()



like = APIRouter()

class likes(BaseModel):
    username: str
    post: int


@like.post("/like",response_class=HTMLResponse)
async def like_post(request:Request, post_id:str=Form(...),token:str=Cookie(None), db:AsyncSession=Depends(get_db) ):
    try:
        ALGORITHM= 'HS256'
        jwt_decoded = jwt.decode(token, os.getenv("JWT_SECRET"),algorithms=[ALGORITHM] )
        username_token = jwt_decoded['username']
        post_pydantic = likes(username=username_token , post=post_id)
        already_liked = await db.scalar(
            select(exists().where(Likes.username==username_token, Likes.post==post_id)

        )
        )
        if already_liked:

            delete_like = await db.execute(
                delete(Likes).where(Likes.username==username_token ,Likes.post==post_id)

            )
            await db.commit()
        else:
            post_db = Likes(**post_pydantic.model_dump())

            db.add(post_db)

            await db.commit()
            await db.refresh(post_db)
        
        referer = request.headers.get("referer")
        return RedirectResponse(url=referer, status_code=302)

    except Exception as err:
        print(err)
        return RedirectResponse(url="/login", status_code=302)
    