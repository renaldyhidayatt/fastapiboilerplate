from fastapi import APIRouter, Depends, HTTPException, status, Response

from utils.hashing import Hashing
from utils.tokenjwt import Token

from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from config.database import engine
from models.users import Users
from .authentity import RegisterUser


router = router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/hello")
def hello():
    return "Hello"


@router.post("/register")
async def register(request: RegisterUser):
    db = Session(engine)

    db_user = Users(
        name=request.name,
        email=request.email,
        password=Hashing.create_hash(request.password),
    )

    db.add(db_user)
    db.commit()

    return Response(
        content="Berhasil membuat user", status_code=status.HTTP_201_CREATED
    )


@router.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends()):
    db = Session(engine)

    user = db.query(Users).filter(Users.email == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )

    if not Hashing.verify_hash(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password"
        )

    access_token = Token.create_access_token(data={"sub": user.email})
    response = {
        "name": user.name,
        "email": user.email,
        "jwtToken": access_token,
    }

    return response
