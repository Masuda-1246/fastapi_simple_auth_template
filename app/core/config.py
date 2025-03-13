import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    PROJECT_NAME: str = "FastAPI Template"
    PROJECT_DESCRIPTION: str = "A reusable FastAPI template"
    VERSION: str = "0.1.0"
    
    # 60分 * 24時間 * 8日 = 8日間
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    
    # CORSの設定 - すでに配列になっているのでそのまま使用
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Pydantic v2では内部のvalidatorで変換する
    @field_validator("CORS_ORIGINS")
    @classmethod
    def validate_cors_origins(cls, cors_origins: List[str]) -> List[str]:
        validated_origins = []
        for origin in cors_origins:
            if isinstance(origin, str):
                # URLの形式チェックを緩める (開発環境用)
                if origin.startswith("http://") or origin.startswith("https://"):
                    validated_origins.append(origin)
                else:
                    # プロトコルが省略されている場合、http://を追加
                    validated_origins.append(f"http://{origin}")
            else:
                validated_origins.append(origin)
        return validated_origins

    # データベース設定
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "app")
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env"
    )


settings = Settings()