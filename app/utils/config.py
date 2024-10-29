import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    #Microservices URLs
    USER_MGMT_URL: str = os.getenv("USER_MGMT_URL", "http://localhost:8000")
    EVENT_MGMT_URL: str = os.getenv("EVENT_MGMT_URL", "http://localhost:8001")
    TICKET_URL: str = os.getenv("TICKET_URL", "http://localhost:8002")

    #Composite Service Configurations
    COMPOSITE_SERVICE_PORT: int = int(os.getenv("COMPOSITE_SERVICE_PORT", 8003))


