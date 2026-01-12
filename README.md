# za2

## Deployment Guide

### 1. Clone the Repository

```bash
git clone https://github.com/shogoorg/za2.git
cd za
```

### 2. Authenticate with Google Cloud

```bash
gcloud auth application-default login
gcloud config set project [YOUR-PROJECT-ID]
export PROJECT_ID=$(gcloud config get project)

```
### 3. Configure Environment

```bash
gcloud services enable \
  bigquery.googleapis.com \
  aiplatform.googleapis.com \
  apikeys.googleapis.com \
  mapstools.googleapis.com \
  cloudresourcemanager.googleapis.com
gcloud beta services mcp enable mapstools.googleapis.com --project=$PROJECT_ID
gcloud beta services mcp enable bigquery.googleapis.com --project=$PROJECT_ID
```

```bash
dos2unix setup/setup_env.sh
chmod +x setup/setup_env.sh
./setup/setup_env.sh
```

### 4. Provision BigQuery

```bash

# Create virtual environment
python3 -m venv .venv

# If the above fails, you may need to install python3-venv:
# apt update && apt install python3-venv

# Activate virtual environment
source .venv/bin/activate
pip install -r requirements.txt
python clean.py
```


```bash
dos2unix setup/setup_bigquery.sh
chmod +x setup/setup_bigquery.sh
./setup/setup_bigquery.sh
```

### 5. Install ADK and Run Agent

```bash

# Create virtual environment
python3 -m venv .venv

# If the above fails, you may need to install python3-venv:
# apt update && apt install python3-venv

# Activate virtual environment
source .venv/bin/activate

pip install -r requirements.txt

# Install ADK
pip install google-adk

# Navigate to the app directory New Terminal
cd adk_agent/

# Run the ADK web interface New Terminal
adk web
```

### 6. Chat with the Agent

*   東京都の再エネ導入目標を教えて
*   新宿区の再エネ導入目標を教えて
*   東京都市町村議会議員公務災害補償等組合の再エネ導入目標を教えて

### 7. Cleanup
```bash
dos2unix cleanup/cleanup_env.sh
chmod +x cleanup/cleanup_env.sh
./cleanup/cleanup_env.sh
```

## Data Logic & Narratives

| Table | Demo Purpose | Narrative Logic |
| :--- | :--- | :--- |
| **`za2`** | **地方公共団体**（都道府県、市区町村、広域連合）の環境施策および再エネ導入目標の回答データを提供。 | **「事実の照合」**: `is_level1`, `is_level2`, `is_union` フラグを用いて団体属性を厳格に識別。フェーズ2で特定された複数の `query_id` に基づき、`IN` 句を用いて関連データを一括取得（Bulk Retrieval）し、データの透明性を確保。 |
| **`za2_vector`** | 自然言語による質問から、関連する施策項目（Topic）を特定するための高次元ベクトルデータおよびメタデータを提供。 | **「意味の検索」**: ユーザーの質問を埋め込みベクトルに変換し、`VECTOR_SEARCH` を実行。膨大な項目から関連性の高い上位20件の `query_id` を最短1ステップで絞り込み、後続のデータ抽出フェーズへ繋げる。 |