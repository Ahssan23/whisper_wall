from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker,declarative_base



DATABASE_URL = "mysql+aiomysql://439426:johnwickmyguy@mysql-whisperwall.alwaysdata.net:3306/whisperwall_ahssan"




engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession,expire_on_commit=False)
Base = declarative_base()


async def get_db():
    async with SessionLocal() as session:
        yield session