from fastapi import FastAPI
from app.views import router

app = FastAPI(title="Library API")

app.include_router(router)
