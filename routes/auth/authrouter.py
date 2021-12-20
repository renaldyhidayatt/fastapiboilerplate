from fastapi import APIRouter
from controllers.auth.entity import auth
from controllers.auth.register.service import registeruser


router = router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/hello")
def hello():
    return "Hello"


@router.post("/register")
def register(request: auth.RegisterUser):
    return registeruser(request=request)
