from fastapi import FastAPI
from app.routers import users, events, health, event_booking
from app.middleware.logging import LoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.utils.config import Config

config = Config()

app = FastAPI(
    title="Composite Service",
    description="API Gateway Composite between UI and Micro-services",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Logging Middleware
app.add_middleware(LoggingMiddleware)

app.include_router(users.router)
app.include_router(events.router)
app.include_router(event_booking.router)
app.include_router(health.router)

@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to the Composite Service!"}
