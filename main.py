from fastapi import FastAPI
from routes.signup import signup
from routes.login import login
from db.db import Base, engine
from routes.home import home 
from routes.upload import post
from routes.likes import like
from routes.comment import comment
from routes.fullPost import fullPost

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("database connected")

app.include_router(signup)
app.include_router(login)
app.include_router(home)
app.include_router(post)
app.include_router(like)
app.include_router(comment)
app.include_router(fullPost)