from utils.utils import utils
#@title tools
from langchain_community.document_loaders import WikipediaLoader
import streamlit as st


def search_wikipedia(state):
    
    """ Retrieve docs from wikipedia """

    try:
            
        # Search
        search_docs = WikipediaLoader(query=state['question'], 
                                    load_max_docs=3).load()

        # Format
        formatted_search_docs = "\n\n---\n\n".join(
            [
                f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("page", "")}"/>\n{doc.page_content}\n</Document>'
                for doc in search_docs
            ]
        )

        with st.expander("Wikipedia取得データ"):
            st.write(formatted_search_docs)


        return {"context": [formatted_search_docs]} 
    except:
        return {"context": ["-"]}