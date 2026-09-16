from pydantic import BaseModel, EmailStr, Field, field_validator


class TaskCreate(BaseModel):
    title: str = Field(max_length=200)
    description: str | None = Field(
        default=None,
        max_length=1000
    )
    completed: bool = False

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty")

        return value


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        max_length=200
    )

    description: str | None = Field(
        default=None,
        max_length=1000
    )

    completed: bool | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if value is None:
            raise ValueError("Title cannot be null")

        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty")

        return value


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool

    model_config = {
        "from_attributes": True
    }

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128
    )


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = {
        "from_attributes": True
    }

# Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

