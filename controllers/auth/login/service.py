from fastapi import HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm
from config.database import engine
from utils import hashing, tokenjwt
from sqlmodel import Session
from models.users import Users


def login(request: OAuth2PasswordRequestForm = Depends()):
    db = Session(engine)

    user = db.query(Users).filter(Users.email == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )

    if not hashing.Hashing.verify_hash(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password"
        )

    access_token = tokenjwt.Token.create_access_token(data={"sub": user.email})
    response = {
        "name": user.name,
        "email": user.email,
        "jwtToken": access_token,
    }

    return response
