from fastapi import HTTPException,Response, status
from starlette.background import BackgroundTasks
from utils import hashing, randomstring
from ..entity.auth import RegisterUser
from config.database import engine
from sqlmodel import Session
from models.users import Users


def registeruser(request: RegisterUser):
    db = Session(engine)

    db_user = Users(
        name=request.name,
        email=request.email,
        password=request.password
    ) 

    db.add(db_user)
    db.commit()

    return Response(content="Berhasil membuat user", status_code=status.HTTP_201_CREATED)