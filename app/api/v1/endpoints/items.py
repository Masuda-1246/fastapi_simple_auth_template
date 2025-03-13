from uuid import UUID
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.crud_item import item as crud_item
from app.models.user import User
from app.schemas.item import Item, ItemCreate, ItemUpdate

router = APIRouter()


@router.get("/", response_model=List[Item])
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    アイテム一覧を取得
    """
    if crud_item.is_superuser(current_user):
        items = crud_item.get_multi(db, skip=skip, limit=limit)
    else:
        items = crud_item.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return items


@router.post("/", response_model=Item)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: ItemCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    新規アイテムを作成
    """
    item = crud_item.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
    return item


@router.get("/{id}", response_model=Item)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    特定のアイテムを取得
    """
    item = crud_item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="アイテムが見つかりません")
    if not crud_item.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="権限がありません")
    return item


@router.put("/{id}", response_model=Item)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    item_in: ItemUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    アイテムを更新
    """
    item = crud_item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="アイテムが見つかりません")
    if not crud_item.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="権限がありません")
    item = crud_item.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.delete("/{id}", response_model=Item)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    アイテムを削除
    """
    item = crud_item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="アイテムが見つかりません")
    if not crud_item.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="権限がありません")
    item = crud_item.remove(db=db, id=id)
    return item
