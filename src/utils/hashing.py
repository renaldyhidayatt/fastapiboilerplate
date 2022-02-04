from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hashing:
    def create_hash(password: str):
        """
        Disini Membuat hash dari bcrypt
        """

        return pwd_cxt.hash(password)

    def verify_hash(hashed_password: str, plain_password: str) -> pwd_cxt:
        """
        Verify Hash password
        """
        return pwd_cxt.verify(plain_password, hashed_password)
