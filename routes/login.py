from fastapi import FastAPI, Depends, Request, Form, APIRouter, Response
from db.db import get_db
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.model import User
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import bcrypt
from jose import jwt
from dotenv import load_dotenv
import os
from datetime import timedelta, datetime, timezone

load_dotenv()

login = APIRouter()
template = Jinja2Templates(directory="templates")


class Login(BaseModel):
    username: str
    password: str


@login.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return template.TemplateResponse('login.html', {"request": request})


@login.post("/login", response_class=HTMLResponse)
async def login_post(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    username: str = Form(...),
    password: str = Form(...)
):
    # Prepare user data
    user_data = Login(username=username, password=password)
    db_user = select(User).where(User.name == user_data.username)
    result = await db.execute(db_user)
    user = result.scalar_one_or_none()

    if not user:
        return template.TemplateResponse(
            "login.html",
            {"request": request, "message": "User not found, try again"}
        )

    hash = user.password.encode('utf-8')
    byte = password.encode("utf-8")

    if bcrypt.checkpw(byte, hash):
    payload = {
        "username": user.name,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=10)
    }
    token = jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm='HS256')

    response = RedirectResponse(url='/', status_code=302)
    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        secure=True,
        samesite="None"
    )
    return response

    else:
        return template.TemplateResponse(
            "login.html",
            {"request": request, "message": "Login failed, try again"}
        )
