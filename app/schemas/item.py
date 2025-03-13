from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


# 共通のプロパティ
class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# 作成時に必要なプロパティ
class ItemCreate(ItemBase):
    title: str


# 更新時のプロパティ
class ItemUpdate(ItemBase):
    pass


# DBから取得するプロパティ
class ItemInDBBase(ItemBase):
    id: UUID
    title: str
    owner_id: UUID

    class ConfigDict:
        from_attributes = True


# APIを通じて返すアイテム情報
class Item(ItemInDBBase):
    pass