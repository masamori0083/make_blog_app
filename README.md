# CodeAnalyzer
🚀 コード解析＆Markdown記事生成ツール

## 概要
このプロジェクトは、ソースコードを貼り付けるだけで、LLM（GPT-4oなど）を活用して解析を行い、技術ブログ用の記事をMarkdown形式で自動生成するアプリです。


## 使用技術
- Python
- Streamlit
- FastAPI
- OpenAI API

## 利用手順
1. バックエンドAPIを起動します。
	 ```bash
	 cd backend
	 uvicorn main:app --host 0.0.0.0 --port 8000
	 ```
2. フロントエンドを起動します。
	 ```bash
	 cd frontend
	 streamlit run app.py
	 ```
3. ブラウザで `http://localhost:8501` にアクセスします。
