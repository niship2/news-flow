from utils.utils import utils
from langchain_community.tools.tavily_search import TavilySearchResults
import streamlit as st


def search_web(state):
    
    """ Retrieve docs from web search """

    try:

        # Search
        tavily_search = TavilySearchResults(max_results=20)
        search_docs = tavily_search.invoke(state['question'] + " news")

        # Format
        formatted_search_docs = "\n\n---\n\n".join(
            [
                f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
                for doc in search_docs
            ]
        )
        #print(formatted_search_docs)
        with st.expander("TavilySearch取得データ"):
            st.write(formatted_search_docs)


        return {"context": [formatted_search_docs]} 
    except:
        return {"context": ["-"]}