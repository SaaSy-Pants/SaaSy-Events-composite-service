from __future__ import annotations

from pydantic import BaseModel, constr, EmailStr


class User(BaseModel):
    UID: str = constr(min_length=1, max_length=5)  # Treat as primary key in logic
    Name: str
    Email: EmailStr = constr(min_length=1, max_length=50)
    PhoneNo: str = constr(min_length=1, max_length=15)
    HashedPswd: str = constr(min_length=1, max_length=255)
    Address: str
    Age: int

    class Config:
        json_schema_extra = {
            "user": {
                "UID": "U001",
                "Name": "John Doe",
                "Email": "johndoe@example.com",
                "PhoneNo": "+1234567890",
                "HashedPswd": "$2b$12$OaUaypuWIjhd7eO7RsWNyuQoJx0hCJ2dx8.AYx5H1P7RBW3DpJIyS",
                "Address": "123 Main St, City, Country",
                "Age": "30"
            }
        }
        orm_mode = True
