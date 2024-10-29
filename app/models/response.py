from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Any

class HATEOASLink(BaseModel):
    rel: str
    href: HttpUrl
    method: str

class HATEOASResponse(BaseModel):
    data: Optional[Any] = None
    message: Optional[str] = None
    links: List[HATEOASLink] = []
