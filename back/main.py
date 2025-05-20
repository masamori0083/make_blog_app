import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from openai import AzureOpenAI

from .schemas import CodeInput, TextInput

# backのルートディレクトリを追加
sys.path.append(str(Path(__file__).parent.resolve()))
load_dotenv()

app = FastAPI()

# Azure OpenAIの設定 (ご自身の設定に変更)
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
subscription_key = os.getenv("AZURE_OPENAI_KEY")
api_version = "2024-12-01-preview"

# モデルを用途別に初期化
analysis_deployment = "o4-mini"
blog_deployment = "gpt-4o"

client_analysis = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

client_blog = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)


def call_llm(client, deployment, prompt, token_limit=4096):
    """
    LLMを呼び出す関数
    """
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_completion_tokens=token_limit,
    )
    return response.choices[0].message.content.strip()


def load_blog_example(path=None):
    """
    ブログ記事の例を読み込む関数
    """
    if path is None:
        path = Path(__file__).parent / "examples" / "blog_sample.md"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


@app.post("/analyze_code")
def analyze_code(input: CodeInput):
    """
    コード解析エンドポイント
    """
    # コード解析プロンプト
    analysis_prompt = f"""
    以下のコードを解析し、機能やアルゴリズムを詳しく日本語で解説してください。

    コード:
    ```
    {input.code}
    ```
    """

    # 解析モデルで解析
    analysis_result = call_llm(client_analysis, analysis_deployment, analysis_prompt)

    # 記事生成プロンプト
    blog_example = load_blog_example()

    markdown_prompt = f"""
    以下は私が書いたブログ記事の例です。私の文章のスタイルや表現方法を参考にしてください。

    ### ブログの例:
    {blog_example}

    ### コード解説:
    {analysis_result}

    上記のコード解説を、例で示した私のブログ記事のスタイルで、読みやすいMarkdown形式の技術ブログ記事として日本語で作成してください。
    見出しや箇条書き、コードブロックを適切に使ってください。
    """

    # 記事生成モデルで記事を生成
    blog_result = call_llm(
        client_blog, blog_deployment, markdown_prompt, token_limit=100000
    )
    return {"markdown": blog_result}


@app.post("/analyze_text")
def analyze_text(input: TextInput):
    """
    テキスト解析エンドポイント
    """
    # テキスト解析プロンプト
    analysis_prompt = f"""
    以下の技術的なテキストの要点を日本語で箇条書きでまとめ、含まれる専門用語を初心者向けに解説してください。

    テキスト:
    ```
    {input.text}
    ```
    """

    # 解析モデルで解析
    analysis_result = call_llm(client_analysis, analysis_deployment, analysis_prompt)

    # 記事生成プロンプト
    blog_example = load_blog_example()

    markdown_prompt = f"""
    以下は私が書いたブログ記事の例です。私の文章のスタイルや表現方法を参考にしてください。

    ### ブログの例:
    {blog_example}

    ### コード解説:
    {analysis_result}

    上記のコード解説を、例で示した私のブログ記事のスタイルで、読みやすいMarkdown形式の技術ブログ記事として日本語で作成してください。
    見出しや箇条書き、コードブロックを適切に使ってください。
    """

    # 記事生成モデルで記事を生成
    blog_result = call_llm(client_blog, blog_deployment, markdown_prompt)
    return {"markdown": blog_result}
