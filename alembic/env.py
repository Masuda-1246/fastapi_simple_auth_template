# alembic/env.py
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Baseクラスとsettingsをインポート
from app.db.session import Base
from app.core.config import settings

# モデルをインポート（これにより、モデルがBaseのメタデータに登録されます）
# 重要: すべてのモデルをインポートしてください
from app.models import user, item

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ターゲットメタデータ - SQLAlchemyモデルのメタデータ
target_metadata = Base.metadata

# データベースURLをsettingsから取得する関数
def get_url():
    return settings.SQLALCHEMY_DATABASE_URI

# SQLAlchemy URLをオーバーライド
config.set_main_option("sqlalchemy.url", get_url())

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # ここでconfigurationを更新して、環境変数から読み込んだURLを使う
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            # 以下のオプションはマイグレーションの動作を制御します
            # 自動的に変更を検出してスキーマを更新するか
            compare_type=True,
            # SQLAlchemyが生成したデフォルト値を検出するか
            compare_server_default=True,
            # 既存のテーブルにnullable=Falseのカラムを追加するときに
            # サーバーデフォルト値を追加するか
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()