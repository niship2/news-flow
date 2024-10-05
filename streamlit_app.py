from utils.utils import utils
import pandas as pd
import streamlit as st

from agents.agent1 import agent_builder

st.set_page_config(layout="wide")

st.title("ニュース検索")

searchword = st.text_input("キーワード入力",value="sakana AI")
MODEL_NAME = st.sidebar.selectbox("モデル選択",["gpt-4o","gemini"])
SELECTED_TOOLS = st.sidebar.multiselect("ツール選択",["search_google_news","search_google_news_JA","search_bing_news","search_wikipedia","search_web"],default=["search_google_news","search_google_news_JA"])

if st.button("検索"):
    st.sidebar.warning("各モジュール未調整のため時間がかかる（2-3分）場合があるので注意")
    graph= agent_builder(SELECTED_TOOLS)

    result = graph.invoke({"question": searchword})

    articles = [[x.title,x.date.strftime("%y-%m-%d"),x.source_url,x.japanese_translation] for x in  result['answer'].content]
    
    article_df = pd.DataFrame(articles,columns=["タイトル","日付","link","日本語訳"])
    st.dataframe(article_df,
    column_config={
        "link": st.column_config.LinkColumn(
            # 表示するカラム名
            "リンク",
            # 表示データのテキスト
            display_text="リンク"
        )
    },)