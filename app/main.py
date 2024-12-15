from fastapi import FastAPI
from app.routers import users, events, health, ticket
from app.middleware.logging import LoggingMiddleware
from app.middleware.auth import AuthMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.utils.config import Config
import uvicorn

config = Config()

app = FastAPI(
    title="Composite Service",
    description="The Composite API acts as a gateway between the UI and all underlying microservices (User, Event, Ticket). It validates JWT, orchestrates calls, and provides a unified interface.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)

app.include_router(users.router)
app.include_router(organizer.router)
app.include_router(events.router)
app.include_router(ticket.router)
app.include_router(health.router)

@app.get("/", tags=["root"])
async def read_root():
    """
    Root endpoint of the Composite Service.
    """
    return {"message": "Welcome to the Composite Service!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8003, reload=True)
