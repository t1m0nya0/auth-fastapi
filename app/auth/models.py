# from passlib.context import CryptContext
#
#
# class UserModel:
#     def __init__(self, email, password):
#         self.email = email
#         self.hashed_password = get_password_hash(password)
#
#     def check_password(self, password):
#         return verify_password(password, self.hashed_password)
#
# # FastAPI app
#
# # Password hashing and verification
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# def get_password_hash(password):
#     return pwd_context.hash(password)
#
# def verify_password(password, hashed_password):
#     return pwd_context.verify(password, hashed_password)

from attrs import define


@define
class UserModel:
    id: int
    email: str
    password: str

    def check_password(self, password):
        return self.password == password
