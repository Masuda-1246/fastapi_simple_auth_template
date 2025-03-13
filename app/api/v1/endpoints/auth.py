from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.crud_user import user as crud_user
from app.core import security
from app.schemas import token as schemas

router = APIRouter()

@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud_user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="メールアドレスまたはパスワードが正しくありません")
    elif not crud_user.is_active(user):
        raise HTTPException(status_code=400, detail="非アクティブなユーザーです")
    return {
        "access_token": security.create_access_token(user.id),
        "token_type": "bearer",
    }

