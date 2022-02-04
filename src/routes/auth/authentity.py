from pydantic import BaseModel


class RegisterUser(BaseModel):
    name: str
    email: str
    password: str

class ForgotPassword(BaseModel):
    email: str

class PasswordReset(BaseModel):
    password: str

