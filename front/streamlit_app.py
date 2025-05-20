import requests
import streamlit as st

st.set_page_config(layout="wide")
st.title("🚀 技術ブログ生成ツール")

# セッション状態初期化
if "markdown" not in st.session_state:
    st.session_state.markdown = ""

# テキスト入力
tab1, tab2 = st.tabs(["📟 コード解析", "📖 テキスト解析"])

# コード解析タブ
with tab1:
    code = st.text_area(
        "🔖 ソースコードをここに貼り付けてください", height=300, key="code_input"
    )

    if st.button("⚙️ コード解析 & 記事生成"):
        if code.strip():
            with st.spinner("コードを解析しています..."):
                response = requests.post(
                    "http://localhost:8000/analyze_code", json={"code": code}
                )

                if response.status_code == 200:
                    st.session_state.markdown = response.json().get("markdown", "")
                    st.success("コード解析が完了しました！")
                else:
                    st.error(
                        "❌ APIサーバーエラーです。バックエンドを確認してください。"
                    )
        else:
            st.warning("コードを入力してください。")

# テキスト解析タブ
with tab2:
    text = st.text_area(
        "🔖 テキストをここに貼り付けてください", height=300, key="text_input"
    )

    if st.button("⚙️ テキスト解析 & 記事生成"):
        if text.strip():
            with st.spinner("テキストを解析しています..."):
                response = requests.post(
                    "http://localhost:8000/analyze_text", json={"text": text}
                )

                if response.status_code == 200:
                    st.session_state.markdown = response.json().get("markdown", "")
                    st.success("テキスト解析が完了しました！")
                else:
                    st.error(
                        "❌ APIサーバーエラーです。バックエンドを確認してください。"
                    )
        else:
            st.warning("テキストを入力してください。")


# Markdownエディターとプレビュー
if st.session_state.markdown:
    # UIを2カラムに分割
    editor_col, preview_col = st.columns(2)

    # MarkdownエディターのUI構成
    with editor_col:
        # Markdownエディター
        st.subheader("📝 生成されたMarkdown記事")
        edited_markdown = st.text_area(
            "Markdownを自由に編集できます", value=st.session_state.markdown, height=600
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
