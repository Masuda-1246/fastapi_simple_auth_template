#!/usr/bin/env python3
"""
DBの初期データを作成するスクリプト
"""
import sys
from pathlib import Path

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.core.config import settings
from app.schemas.user import UserCreate
from app.schemas.item import ItemCreate
from app.crud.crud_user import user
from app.crud.crud_item import item


def init_db(db: Session) -> None:
    # スーパーユーザーがいない場合は作成
    super_user = user.get_by_email(db, email="admin@example.com")
    if not super_user:
        user_in = UserCreate(
            email="admin@example.com",
            password="password",
            is_superuser=True,
            full_name="Initial Admin",
        )
        super_user = user.create(db, obj_in=user_in)
        print(f"スーパーユーザーを作成しました: {super_user.email}")

    # 一般ユーザーがいない場合は作成
    normal_user = user.get_by_email(db, email="user@example.com")
    if not normal_user:
        user_in = UserCreate(
            email="user@example.com",
            password="password",
            is_superuser=False,
            full_name="Normal User",
        )
        normal_user = user.create(db, obj_in=user_in)
        print(f"一般ユーザーを作成しました: {normal_user.email}")

    # サンプルアイテムの作成
    if not item.get_multi_by_owner(db, owner_id=normal_user.id):
        for i in range(3):
            item_in = ItemCreate(
                title=f"サンプルアイテム {i+1}",
                description=f"これはサンプルアイテム {i+1} の説明です。",
            )
            item.create_with_owner(db, obj_in=item_in, owner_id=normal_user.id)
        print(f"{normal_user.email} 用のサンプルアイテムを作成しました")


def main() -> None:
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
