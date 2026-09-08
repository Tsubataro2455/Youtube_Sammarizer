"""YouTube動画の字幕を要約するアプリケーション。

Claude APIを使用して、YouTube動画の字幕を日本語で要約します。
字幕が存在しない動画は処理できません。
"""

import streamlit as st
import re
import json
import requests
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def init_page():
    """Streamlitページの初期設定"""
    st.set_page_config(
        page_title="Youtube Summarizer",
        page_icon="🎞️"
    )
    st.header("Youtube Summarizer 🎞️")
    st.sidebar.title("Options")


def select_model():
    """サイドバーからClaudeモデルを選択してインスタンス化"""
    model_name = st.sidebar.radio(
        "Choose a model:",
        ("claude-haiku-4-5", "claude-sonnet-4-6")
    )
    st.session_state.model_name = model_name
    st.session_state.max_token = 4000

    return ChatAnthropic(model=model_name, temperature=0)


def get_video_metadata(url):
    """YouTubeのメタデータ（タイトル、投稿者）を取得"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()

        json_ld_pattern = r'<script[^>]*type="application/ld\+json"[^>]*>({.*?"@type":"VideoObject".*?})</script>'
        match = re.search(json_ld_pattern, response.text, re.DOTALL)

        if match:
            data = json.loads(match.group(1))
            title = data.get('name', 'Unknown Title')
            author = data.get('author', {}).get('name', 'Unknown Author')
            return title, author
    except Exception:
        pass

    return None, None


def get_document(url):
    """YouTube URLから動画の字幕を取得してチャンク分割"""
    with st.spinner("Fetching Content ..."):
        try:
            loader = YoutubeLoader.from_youtube_url(
                url,
                add_video_info=False,
                language=['en', 'ja']
            )

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=4000,
                chunk_overlap=0,
                separators=["\n\n", "\n", " ", ""]
            )

            docs = loader.load_and_split(text_splitter=text_splitter)
            if not docs:
                raise ValueError("字幕が見つかりませんでした。")

            return docs

        except Exception as e:
            raise ValueError(f"動画の取得に失敗しました: {str(e)}")


def summarize(model, docs):
    """LangChainのmap_reduceチェーンで字幕を要約"""
    prompt_template = """YouTube動画の字幕を簡潔な日本語で要約してください。

{text}

日本語での要約:
"""
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

    chain = load_summarize_chain(
        model,
        chain_type="map_reduce",
        verbose=True,
        map_prompt=prompt,
        combine_prompt=prompt
    )

    response = chain(
        {
            "input_documents": docs,
            "token_max": st.session_state.max_token
        },
        return_only_outputs=True
    )

    return response['output_text']


def main():
    """アプリケーションのメインロジック"""
    init_page()
    model = select_model()

    input_container = st.container()
    output_container = st.container()

    with input_container:
        url = st.text_input("Youtube URL: ", key="input")

        if not url:
            st.info("YouTubeのURLを入力してください。")
            return

        try:
            docs = get_document(url)
            if not docs:
                st.error("字幕を取得できませんでした。字幕が含まれている動画をお試しください。")
                return

            with st.spinner("要約を生成中..."):
                output_text = summarize(model, docs)

        except ValueError as e:
            st.error(f"エラー: {str(e)}")
            return

    if output_text:
        with output_container:
            title, author = get_video_metadata(url)

            if title or author:
                st.markdown(f"**{title or '不明なタイトル'}** - {author or '不明な投稿者'}")
                st.markdown("---")

            st.markdown("## 要約")
            st.write(output_text)

            st.markdown("---")
            st.markdown("## 元のテキスト")
            st.write(docs)


if __name__ == '__main__':
    main()