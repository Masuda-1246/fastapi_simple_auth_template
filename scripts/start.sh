#!/bin/bash
set -e

# データベースのマイグレーションを実行
alembic upgrade head

# FastAPIアプリケーションの起動
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
