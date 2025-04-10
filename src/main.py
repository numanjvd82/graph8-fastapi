from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from contextlib import asynccontextmanager
from .routes.company_router import router as company_router
from .routes.contact_router import router as contact_router
from .config import FRONTEND_URL

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield  

    # Cleanup
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.mount(
    "/src/static",
    StaticFiles(directory="src/static"),
    name="static",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],  # Your React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Welcome to the FastAPI backend!"}
    

app.include_router(company_router)
app.include_router(contact_router)

