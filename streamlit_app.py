from utils.utils import utils
import pandas as pd
import streamlit as st
import streamlit_mermaid as stmd

from agents.agent1 import agent_builder


st.set_page_config(layout="wide")

st.title("ニュース検索")

searchword = st.text_input("キーワード入力",value="sakana AI")
#MODEL_NAME = st.sidebar.selectbox("モデル選択",["gpt-4o","gemini"])
SELECTED_TOOLS = st.sidebar.multiselect("ツール選択",["search_google_news","search_google_news_JA","search_bing_news","search_wikipedia","search_tavily","search_youcom"],default=["search_google_news","search_google_news_JA"])
TIME_OP= st.sidebar.selectbox("期間選択(※)",["直近24時間","直近1週間","過去2週間","直近1ヶ月","過去1年"],index=2)
st.sidebar.write("※：期間選択はGoogleNews,BingNewsのみ指定可能")

if st.button("検索"):
    st.sidebar.warning("抽出に時間がかかる場合があるので注意。今後改善していきます")
    graph= agent_builder(SELECTED_TOOLS)

    #with st.sidebar.expander("抽出フロー"):
        #st.write(graph.get_graph().print_ascii())
        #stmd.st_mermaid(graph.get_graph().draw_mermaid())
        #st.markdown(graph.get_graph().draw_mermaid())


    result = graph.invoke({"question": searchword,"time_op":TIME_OP})

    articles = [[x.title,x.date.strftime("%y-%m-%d"),x.source_url,x.japanese_translation] for x in  result['answer'].content]

    st.write("記事まとめ：これらの記事を要約して３行にまとめます（未実装）")
    
    article_df = pd.DataFrame(articles,columns=["タイトル","日付","link","日本語訳"]).sort_values(by="日付",ascending=False)
    st.dataframe(article_df[["link","日付","日本語訳","タイトル"]],
    column_config={
        "link": st.column_config.LinkColumn(
            # 表示するカラム名
            "リンク",
            # 表示データのテキスト
            display_text="リンク"
        )
    },
    #use_container_width=True,
    hide_index=True)

    with st.expander("参考：全取得データ"):
        st.write(result['context'])