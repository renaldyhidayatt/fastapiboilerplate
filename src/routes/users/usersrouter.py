from fastapi import APIRouter, Depends, Response, status

from utils.tokenjwt import Token
from utils.hashing import Hashing
from database.models.users import Users
from sqlmodel import Session
from config.database import engine

from .usersentity import UserEntity

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def getAll(current_users=Depends(Token.get_currentUser)):
    db = Session(engine)

    return db.query(Users).all()


@router.get("/{id}")
async def getById(id: int):
    db = Session(engine)

    db_result = db.query(Users).filter(Users.id == id).first()

    return db_result


@router.post("/")
async def createUsers(request: UserEntity):
    db = Session(engine)
    db_create = Users(
        name=request.name,
        email=request.email,
        password=Hashing.create_hash(request.password),
    )

    db.add(db_create)
    db.commit()

    return Response(content="Bisa", status_code=status)


@router.put("/{id}")
async def updateUsers(id: int, request: UserEntity):
    db = Session(engine)
    db_update = db.query(Users).filter(Users.id == id).first()

    db_update.name = request.name
    db_update.email = request.email
    db_update.password = Hashing.create_hash(request.password)

    db.commit()

    return Response(content="Update", status_code=status.HTTP_200_OK)


@router.delete("/{id}")
async def deleteUsers(id: int):
    db = Session(engine)

    db_delete = db.query(Users).filter(Users.id == id).first()

    db.delete(db_delete)
    db.commit()

    return Response(content="Delete Users", status_code=status.HTTP_200_OK)
