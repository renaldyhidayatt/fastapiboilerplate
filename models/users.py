from typing import Optional
from sqlmodel import SQLModel, Field


class Users(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    name: str
    email: str
    password: str
