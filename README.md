# fastapi_simple_auth_template

このプロジェクトは、FastAPI フレームワークを使用した RESTful API の開発用テンプレートです。PostgreSQL データベース、Alembic によるマイグレーション、Docker による開発環境などが含まれています。

## 特徴

- **モジュール化されたアーキテクチャ**: 拡張性と保守性に優れた構造設計
- **SQLAlchemy ORM**: データベースアクセスの抽象化
- **Pydantic モデル**: データバリデーションとシリアライゼーション
- **JWT 認証**: セキュアなユーザー認証
- **Alembic マイグレーション**: データベーススキーマの変更管理
- **Docker & Docker Compose**: コンテナ化された開発/本番環境
- **UUID ベースの ID**: セキュリティ向上のための予測不可能な ID

## 必要条件

- Docker と Docker Compose
- Git

## セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/Masuda-1246/fastapi_simple_auth_template.git
cd fastapi_simple_auth_template
```

### 2. 環境変数の設定

`.env.example` ファイルを `.env` にコピーし、必要に応じて環境変数を設定します。

```bash
cp .env.example .env
```

### 3. Docker コンテナのビルドと起動

```bash
docker-compose build
docker-compose up -d
```

これにより以下のサービスが起動します：
- Web サーバー (FastAPI): http://localhost:8000
- PostgreSQL データベース
- Adminer (データベース管理): http://localhost:8080

### 4. マイグレーションの実行

コンテナが起動したら、データベースマイグレーションを実行します：

```bash
docker-compose exec web alembic upgrade head
```

## 開発ワークフロー

### API サーバーの起動

```bash
docker-compose up -d
```

FastAPI サーバーは自動的にコードの変更を検出し、リロードします。

### API ドキュメントの確認

- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

### データベースの管理

Adminer を使用してデータベースを管理できます：
- URL: http://localhost:8080
- システム: PostgreSQL
- サーバー: db
- ユーザー名: postgres (または .env で設定した値)
- パスワード: postgres (または .env で設定した値)
- データベース: app (または .env で設定した値)

### マイグレーションの作成と適用

モデルを変更した後、マイグレーションを作成します：

```bash
docker-compose exec web alembic revision --autogenerate -m "説明文"
```

作成されたマイグレーションスクリプトを確認し、必要に応じて編集します：

```bash
# マイグレーションファイルの確認
ls -la alembic/versions/
```

マイグレーションを適用します：

```bash
docker-compose exec web alembic upgrade head
```

マイグレーションを元に戻す場合：

```bash
docker-compose exec web alembic downgrade -1  # 一つ前の状態に戻す
# または
docker-compose exec web alembic downgrade <revision>  # 特定のリビジョンに戻す
```

### テストの実行

```bash
docker-compose exec web pytest
```

特定のテストを実行する場合：

```bash
docker-compose exec web pytest tests/test_api/v1/test_users.py -v
```

## プロジェクト構造

```
fastapi-template/
│
├── app/                      # アプリケーションのメインパッケージ
│   ├── __init__.py
│   ├── main.py               # FastAPIアプリケーションのエントリーポイント
│   ├── api/                  # APIエンドポイント
│   │   ├── deps.py           # 依存性（DIコンテナなど）
│   │   └── v1/               # APIバージョン1
│   │       ├── endpoints/    # 各エンドポイント
│   │       └── router.py     # ルーター設定
│   │
│   ├── core/                 # コアモジュール
│   │   ├── config.py         # 設定管理
│   │   └── security.py       # セキュリティ関連
│   │
│   ├── crud/                 # CRUD操作
│   │   ├── base.py           # 基本CRUD操作
│   │   └── crud_user.py      # ユーザーCRUD
│   │
│   ├── db/                   # データベース設定
│   │   └── session.py        # DB接続セッション
│   │
│   ├── models/               # SQLAlchemyモデル
│   │   ├── user.py           # ユーザーモデル
│   │   └── item.py           # アイテムモデル
│   │
│   ├── schemas/              # Pydanticスキーマ
│   │   ├── token.py          # トークンスキーマ
│   │   ├── user.py           # ユーザースキーマ
│   │   └── item.py           # アイテムスキーマ
│   │
│   └── services/             # ビジネスロジック
│
├── alembic/                  # マイグレーション
│   ├── versions/             # マイグレーションファイル
│   ├── env.py                # Alembic環境設定
│   └── script.py.mako        # マイグレーションテンプレート
│
├── tests/                    # テスト
│   ├── conftest.py           # テスト設定
│   └── test_api/             # APIテスト
│
├── .env.example              # 環境変数テンプレート
├── .gitignore                # Gitの無視ファイル設定
├── docker-compose.yml        # Docker Compose設定
├── Dockerfile                # Dockerイメージ設定
├── pyproject.toml            # Pythonプロジェクト設定
├── requirements.txt          # 依存関係
├── requirements-dev.txt      # 開発用依存関係
└── README.md                 # このファイル
```

## トラブルシューティング

### マイグレーションエラー

マイグレーション中にエラーが発生した場合、以下を試してください：

```bash
# Alembicの現在の状態を確認
docker-compose exec web alembic current

# PostgreSQLデータベースに直接接続して状態を確認
docker-compose exec db psql -U postgres -d app

# 問題が解決しない場合は、データベースをリセットして再度マイグレーションを実行
docker-compose down -v
docker-compose up -d
docker-compose exec web alembic upgrade head
```

### コンテナ内でのデバッグ

コンテナ内でコマンドを実行してデバッグする：

```bash
# シェルにアクセス
docker-compose exec web bash

# パッケージの確認
pip list

# Pythonインタープリタでコードをテスト
python -c "from app.db.session import Base; print(Base.metadata.tables.keys())"
```
