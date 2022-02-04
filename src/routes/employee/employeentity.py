from typing import Optional
from sqlmodel import SQLModel, Field

class EmployeeEntity(SQLModel, table=True):
    name: str
    jobs: str
    address: str
