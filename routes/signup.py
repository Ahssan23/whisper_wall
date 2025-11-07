from fastapi import APIRouter ,Request,Form,Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from models.model import User
from db.db import get_db
import bcrypt
from pydantic import BaseModel,EmailStr, ValidationError



signup = APIRouter()


template = Jinja2Templates(directory='templates')


class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str





@signup.get("/signup", response_class=HTMLResponse)
def signup_get(request:Request):
    
    return template.TemplateResponse("signup.html", {"request":request})

@signup.post("/signup",response_class=HTMLResponse)
async def signup_post(request:Request,db:AsyncSession=Depends(get_db) ,email:str=Form(...),username:str=Form(...), password:str=Form(...)):
    try:

        byte = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_pass = bcrypt.hashpw(byte, salt)

        user_data = UserCreate(name=username, password=hashed_pass,email=email)
        db_user = User(**user_data.model_dump())

        db.add(db_user)
        await db.commit()
        
        await db.refresh(db_user)

        return RedirectResponse(url='/login',status_code=302)
    
    except ValidationError as err:
        print(err)
        return template.TemplateResponse("signup.html", {"request":request, "message":"validation failed"})
    except IntegrityError as err:
        return template.TemplateResponse("signup.html", {"request":request, "message":"username or email is already taken, choose different one."})

        

