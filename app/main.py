import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health, user_management

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

app.include_router(health.health_router, prefix='/health')
app.include_router(user_management.user_management_router, prefix='/user_management')

@app.get("/")
async def root():
    return {"message": "Hello from the Composite Microservice!"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8003)