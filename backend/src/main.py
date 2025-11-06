from sqlalchemy import text
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    from database.session import _engine
    from database.models import Base
    async with _engine.begin() as conn:
        await conn.execute(text('SELECT 1'))
        await conn.run_sync(Base.metadata.create_all)
    yield

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(lifespan=lifespan)

from dependencies import db_session_middleware
app.middleware("http")(db_session_middleware)

from routers.doctor import router as DRouter
from routers.pacient import router as PRouter
from routers.user import router as URouter

app.include_router(DRouter)
app.include_router(PRouter)
app.include_router(URouter)

if __name__ == "__main__":
    uvicorn.run(app, host="26.167.186.152")