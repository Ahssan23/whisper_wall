from fastapi import APIRouter,Request,Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from jose import jwt
from fastapi.templating import Jinja2Templates
from sqlalchemy import insert
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
# from models.model import post
from dotenv import load_dotenv
from db.db import get_db
from models.model import Post, Likes



home = APIRouter()

template = Jinja2Templates(directory="templates")


@home.get("/", response_class=HTMLResponse)
async def home_get(request:Request, db:AsyncSession=Depends(get_db)):
    posts= await db.execute(select(Post))
    likes = await db.execute(select(Likes))
    result = posts.scalars().all()
    result_like= likes.scalars().all()


    return template.TemplateResponse("home.html", {"request":request,"likes":result_like, "result":result})



