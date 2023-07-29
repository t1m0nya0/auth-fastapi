from fastapi import FastAPI, HTTPException
import jwt

from .auth.serializers import (RefreshOutput, LoginOutput,
                               RefreshInput, LoginInput,
                               RegisterInput, RegisterOutput)
from .auth.utils import create_jwt_token, JWT_SECRET
from .auth.models import UserModel

app = FastAPI()

user_db = [
    UserModel(1, "user@example.com", "Test0001")
]


@app.post("/login", response_model=LoginOutput)
def post_login(login_input: LoginInput):
    email = login_input.email
    password = login_input.password
    try:
        user = next(u for u in user_db if u.email == email)
        if not user.check_password(password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
    except StopIteration:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    jwt_token = create_jwt_token(user.id)
    return jwt_token


@app.post("/refresh_token", response_model=RefreshOutput)
def post_refresh_token(refresh_input: RefreshInput):
    refresh_token = refresh_input.refresh_token
    try:
        payload = jwt.decode(refresh_token, key=JWT_SECRET, algorithms="HS256")
        if payload['type'] != 'refresh':
            raise HTTPException(status_code=400, detail="Token type is not refresh!")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Refresh token is expired!")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Refresh token is invalid!")

    user_id = payload['user_id']

    try:
        user = next(u for u in user_db if u.id == user_id)
    except StopIteration:
        raise HTTPException(status_code=400, detail="Invalid user_id in the token!")

    new_jwt_token = create_jwt_token(user.id)
    return new_jwt_token


@app.post("/register", response_model=RegisterOutput)
def register(register_input: RegisterInput):
    email = register_input.email
    password1 = register_input.password1
    password2 = register_input.password2

    # Check if the passwords match
    if password1 != password2:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Check if a user with this email already exists
    if any(user.email == email for user in user_db):
        raise HTTPException(status_code=400, detail="User with this email already exists")

    # Create a new user and add it to the database (for testing purposes)
    new_user = UserModel(id=len(user_db) + 1, email=email, password=password1)
    user_db.append(new_user)
    print(user_db)
    return {"message": "User successfully registered"}
