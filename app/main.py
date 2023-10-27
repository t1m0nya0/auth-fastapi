import jwt
from databases import Database
from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI, HTTPException

from .auth.serializers import (RefreshOutput, LoginOutput,
                               RefreshInput, LoginInput,
                               RegisterInput, RegisterOutput)
from .auth.utils import create_jwt_token, JWT_SECRET
from .auth.models import UserModel

app = FastAPI()
# URL для PostgreSQL (измените его под свою БД)
DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"

database = Database(DATABASE_URL)


# Модель User для валидации входных данных
class UserCreate(BaseModel):
    username: str
    email: str


# Модель User для валидации исходящих данных - чисто для демонстрации (обычно входная модель шире чем выходная, т.к. на вход мы просим, например, пароль, который обратно не возвращаем, и другое, что не обязательно возвращать)
class UserReturn(BaseModel):
    username: str
    email: str
    id: Optional[int] = None


# тут устанавливаем условия подключения к базе данных и отключения - можно использовать в роутах контекстный менеджер async with Database(...) as db: etc
@app.on_event("startup")
async def startup_database():
    await database.connect()


@app.on_event("shutdown")
async def shutdown_database():
    await database.disconnect()


# создание роута для создания юзеров
@app.post("/users/", response_model=UserReturn)
async def create_user(user: UserCreate):
    query = "INSERT INTO users (username, email) VALUES (:username, :email) RETURNING id"
    values = {"username": user.username, "email": user.email}
    try:
        user_id = await database.execute(query=query, values=values)
        return {**user.dict(), "id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create user")


# маршрут для получения информации о юзере по ID
@app.get("/user/{user_id}", response_model=UserReturn)
async def get_user(user_id: int):
    query = "SELECT * FROM users WHERE id = :user_id"
    values = {"user_id": user_id}
    try:
        result = await database.fetch_one(query=query, values=values)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch user from database")
    if result:
        return UserReturn(username=result["username"], email=result["email"], id=result["id"])
    else:
        raise HTTPException(status_code=404, detail="User not found")


# роут для обновления информации о юзере по ID
@app.put("/user/{user_id}", response_model=UserReturn)
async def update_user(user_id: int, user: UserCreate):
    query = "UPDATE users SET username = :username, email = :email WHERE id = :user_id"
    values = {"user_id": user_id, "username": user.username, "email": user.email}
    try:
        await database.execute(query=query, values=values)
        return {**user.dict(), "id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update user in database")


# роут для удаления информации о юзере по ID
@app.delete("/user/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    query = "DELETE FROM users WHERE id = :user_id RETURNING id"
    values = {"user_id": user_id}
    try:
        deleted_rows = await database.execute(query=query, values=values)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete user from database")
    if deleted_rows:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

#
# user_db = [
#     UserModel(1, "user@example.com", "Test0001")
# ]
#
#
# @app.post("/login", response_model=LoginOutput)
# def post_login(login_input: LoginInput):
#     email = login_input.email
#     password = login_input.password
#     try:
#         user = next(u for u in user_db if u.email == email)
#         if not user.check_password(password):
#             raise HTTPException(status_code=401, detail="Invalid email or password")
#     except StopIteration:
#         raise HTTPException(status_code=401, detail="Invalid email or password")
#
#     jwt_token = create_jwt_token(user.id)
#     return jwt_token
#
#
# @app.post("/refresh_token", response_model=RefreshOutput)
# def post_refresh_token(refresh_input: RefreshInput):
#     refresh_token = refresh_input.refresh_token
#     try:
#         payload = jwt.decode(refresh_token, key=JWT_SECRET, algorithms="HS256")
#         if payload['type'] != 'refresh':
#             raise HTTPException(status_code=400, detail="Token type is not refresh!")
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=400, detail="Refresh token is expired!")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=400, detail="Refresh token is invalid!")
#
#     user_id = payload['user_id']
#
#     try:
#         user = next(u for u in user_db if u.id == user_id)
#     except StopIteration:
#         raise HTTPException(status_code=400, detail="Invalid user_id in the token!")
#
#     new_jwt_token = create_jwt_token(user.id)
#     return new_jwt_token
#
#
# @app.post("/register", response_model=RegisterOutput)
# def register(register_input: RegisterInput):
#     email = register_input.email
#     password1 = register_input.password1
#     password2 = register_input.password2
#
#     # Check if the passwords match
#     if password1 != password2:
#         raise HTTPException(status_code=400, detail="Passwords do not match")
#
#     # Check if a user with this email already exists
#     if any(user.email == email for user in user_db):
#         raise HTTPException(status_code=400, detail="User with this email already exists")
#
#     # Create a new user and add it to the database (for testing purposes)
#     new_user = UserModel(id=len(user_db) + 1, email=email, password=password1)
#     user_db.append(new_user)
#     print(user_db)
#     return {"message": "User successfully registered"}
