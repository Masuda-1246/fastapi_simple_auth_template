from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict


# 共通のプロパティ
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


# 作成時に必要なプロパティ（パスワードが必要）
class UserCreate(UserBase):
    email: EmailStr
    password: str


# 更新時のプロパティ（すべてオプショナル）
class UserUpdate(UserBase):
    password: Optional[str] = None


# DBから取得するプロパティ（パスワードは含まない）
class UserInDBBase(UserBase):
    id: Optional[UUID] = None

    class ConfigDict:
        from_attributes = True


# APIを通じて返すユーザー情報
class User(UserInDBBase):
    pass


# DBに格納されるユーザー情報（ハッシュ化されたパスワードを含む）
class UserInDB(UserInDBBase):
    hashed_password: str