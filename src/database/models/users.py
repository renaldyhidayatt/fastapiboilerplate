from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class Users(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    name: str
    email: str
    password: str
    verifyCationToken: Optional[str] = None
    verifyDate: datetime = Field(default_factory=datetime.now, nullable=True)

    passwordResetDate: datetime = Field(default_factory=datetime.now, nullable=True)
    resetPasswordToken: Optional[str] = None
