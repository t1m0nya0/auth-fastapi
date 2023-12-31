from pydantic import BaseModel, EmailStr, validator, SecretStr


class LoginOutput(BaseModel):
    access: str
    refresh: str


class RefreshOutput(BaseModel):
    access: str
    refresh: str


class PasswordValidator(str):
    min_length = 8

    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < cls.min_length:
            raise ValueError(f"The password must contain at least {cls.min_length} characters")
        if not any(char.isupper() for char in value):
            raise ValueError("The password must contain at least one uppercase letter")
        if not any(char.isdigit() for char in value):
            raise ValueError("The password must contain at least one digit")
        return value


class LoginInput(BaseModel):
    email: EmailStr
    password: str = "Test0001"

    @validator("password", always=True)
    @classmethod
    def validate_password(cls, value):
        return PasswordValidator.validate_password(value)


class RefreshInput(BaseModel):
    refresh_token: str


class RegisterInput(BaseModel):
    email: EmailStr = "user1@example.com"
    password1: str = "Test0001"
    password2: str = "Test0001"

    @validator("password1", always=True)
    @classmethod
    def validate_password1(cls, value):
        return PasswordValidator.validate_password(value)

    @validator("password2", always=True)
    @classmethod
    def validate_password2(cls, value):
        return PasswordValidator.validate_password(value)


class RegisterOutput(BaseModel):
    message: str
