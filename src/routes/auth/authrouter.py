from fastapi import APIRouter, Depends, HTTPException, status, Response, HTTPException

from utils.hashing import Hashing
from utils.tokenjwt import Token

from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from config.database import engine
from config.mail import Mail
from database.models.users import Users
from .authentity import RegisterUser, ForgotPassword, PasswordReset
from datetime import datetime
from starlette.background import BackgroundTasks
from utils.randomstring import randomGenerateString


router = router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/hello")
def hello():
    return "Hello"


@router.post("/register")
async def register(request: RegisterUser, backgroundTask: BackgroundTasks):
    db = Session(engine)

    db_user = Users(
        name=request.name,
        email=request.email,
        password=Hashing.create_hash(request.password),
    )

    verifyToken = randomGenerateString(30)

    db_user.verifyCationToken = verifyToken

    db.add(db_user)
    db.commit()

    mail = Mail()

    backgroundTask.add_task(
        mail.sendEmailVerify, verifyToken=str(verifyToken), email=str(request.email)
    )

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


@router.post("/forgot")
async def forgotPasswordEmail(forgot: ForgotPassword, backgroundTask: BackgroundTasks):
    db = Session(engine)

    db_email = db.query(Users).filter(Users.email == forgot.email).first()

    if not db_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email not found"
        )

    random_gen = randomGenerateString(30)

    db_email.resetPasswordToken = random_gen

    db.commit()

    mail = Mail()

    backgroundTask.add_task(
        mail.sendForgotPasswordEmail,
        resetPasswordToken=random_gen,
        email=db_email.email,
    )

    return Response(content="Bisa Coy", status_code=status.HTTP_200_OK)


@router.post("/reset")
async def resetPassword(token, request: PasswordReset):
    db = Session(engine)

    db_email = db.query(Users).filter(Users.resetPasswordToken == token).first()

    if not db_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token not found"
        )

    db_email.password = Hashing.create_hash(request.password)
    db_email.passwordResetDate = datetime.now()
    db_email.resetPasswordToken = None

    db.commit()

    return Response(content="Bisa coy", status_code=status.HTTP_200_OK)


@router.post("/{token}")
async def verifyEmailToken(token: str):
    db = Session(engine)

    db_verifyToken = db.query(Users).filter(Users.verifyCationToken == token).first()

    if not db_verifyToken:
        return "Error Token Typo"

    db_verifyToken.verifyDate = datetime.now()
    db_verifyToken.verifyCationToken = "kosong"

    db.commit()

    return Response(content="Verify Email Token", status_code=status.HTTP_200_OK)
