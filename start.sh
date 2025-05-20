# バックエンドを起動（バックグラウンドで）
uvicorn back.main:app --reload &

# フロントエンド（Streamlit）を起動
streamlit run front/streamlit_app.py

# Ctrl+Cで終了したらバックエンドも終了する
trap "pkill uvicorn" EXIT