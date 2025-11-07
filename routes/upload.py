from fastapi import APIRouter, Request, Response, Form,Depends, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.future import select 
from jose import jwt
from models.model import Post
from db.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
from pydantic import BaseModel
from sqlalchemy import insert
import os 
from sqlalchemy.exc import DataError


load_dotenv()


post = APIRouter()

templates = Jinja2Templates(directory="templates")


class AddPost(BaseModel):
    username:str
    title:str
    content:str

@post.get("/post", response_class=HTMLResponse)
def post_get(request:Request):
    return templates.TemplateResponse('upload.html', {"request":request})



@post.post("/post",  response_class=HTMLResponse)
async def post_post(request:Request,token:str=Cookie(None), title :str=Form(...), content:str=Form(...), db:AsyncSession=Depends(get_db)):
    try:
        ALGORITHM='HS256'
        jwt_token = jwt.decode(
                token, os.getenv("JWT_SECRET"), algorithms=[ALGORITHM]
            )
        username = jwt_token['username']
        print('USERNAME', username)

        post_pydantic = AddPost(username=username, title=title, content=content)
        add_db = Post(**post_pydantic.model_dump())

        db.add(add_db)
        await db.commit()
        await db.refresh(add_db)




        return RedirectResponse(url="/", status_code=302)
    except DataError as e:

        return templates.TemplateResponse("upload.html", {"request":request, "message":"title can be 30 characters long maximum and blog can be 1000 characters long maximum"})
    except Exception as error:
        print(error)
        return RedirectResponse(url="/login", status_code=302)
    
        