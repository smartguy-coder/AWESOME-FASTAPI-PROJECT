from pydantic import BaseModel, Field, EmailStr


class AuthDetails(BaseModel):
    login: EmailStr = Field(examples=['andrebojarski77@gmial.com'])
    password: str = Field(min_length=12, max_length=30, examples=['n5j3598r190r43&'])


class AuthRegistered(BaseModel):
    success: bool = Field(examples=['True'])

