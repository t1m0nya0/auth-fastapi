# from fastapi import FastAPI, HTTPException
# import jwt
#
# from .serializers import (RefreshOutput, LoginOutput,
#                                RefreshInput, LoginInput)
# from .utils import create_jwt_token, JWT_SECRET
# from .models import UserModel
#
# app = FastAPI()
#
# user_db = [
#     UserModel(1, "test@example.com", "password")
# ]
#
#
# @app.post("/login", response_model=LoginOutput)
# def post_login(login_input: LoginInput):
#     email = login_input.email
#     password = login_input.password
#
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
#
#     try:
#         payload = jwt.decode(refresh_token, key=JWT_SECRET)
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
