# Dockerfile
FROM python:3.9

WORKDIR /app/

# 必要なパッケージをインストール
COPY requirements.txt .

# 明示的にPydantic v2とpydantic-settingsをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコピー
COPY . /app/

# コンテナ実行時のコマンド
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]