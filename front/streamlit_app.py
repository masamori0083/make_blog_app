import requests
import streamlit as st

st.set_page_config(layout="wide")

st.title("🚀 コード解析 & Markdown記事作成ツール")

# コード入力用テキストエリア
code = st.text_area("🔖 解析したいコードをここに貼り付けてください", height=300)

# セッション状態初期化
if "markdown" not in st.session_state:
    st.session_state.markdown = ""


# 解析&記事作成ボタン
if st.button("⚙️ 解析 & 記事生成") and code.strip():
    with st.spinner("解析中..."):
        # APIリクエスト
        response = requests.post("http://localhost:8000/analyze", json={"code": code})

        # レスポンスの処理
        if response.status_code == 200:
            st.session_state.markdown = response.json().get("markdown", "")
            st.success("解析が完了しました！")
        else:
            st.error("❌ APIサーバーエラーです。バックエンドを確認してください。")

# Markdownエディターとプレビュー
if st.session_state.markdown:
    # UIを2カラムに分割
    editor_col, preview_col = st.columns(2)

    # MarkdownエディターのUI構成
    with editor_col:
        # Markdownエディター
        st.subheader("📝 生成されたMarkdown記事")
        edited_markdown = st.text_area(
            "生成されたMarkdown記事", value=st.session_state.markdown, height=600
        )

    # プレビューのUI構成
    with preview_col:
        st.subheader("🔍 プレビュー")
        st.markdown(edited_markdown, unsafe_allow_html=True)

    # Markdownダウンロードボタン
    st.download_button(
        label="📥 Markdownをダウンロード",
        data=edited_markdown,
        file_name="generated_article.md",
        mime="text/markdown",
    )
