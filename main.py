from fastapi import FastAPI
from src.api.message_api import router as api_router

app = FastAPI()

# Include the API router
app.include_router(api_router)
