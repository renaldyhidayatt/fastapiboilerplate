from typing import Optional
from sqlmodel import SQLModel, Field


class Employee(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    name: str
    jobs: str
    address: str
