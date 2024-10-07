import streamlit as st
import pandas as pd
import requests
import datetime
from datetime import datetime
from utils.utils import return_period


def exclude_site(url):
    if "yahoo" in url:
        return False
    else:
        return True



def get_bing_news(word, time_op, additional_word):
    # Add your Bing Search V7 subscription key and endpoint to your environment variables.
    subscription_key = st.secrets["BING_subscription_key"]
    endpoint = st.secrets["BING_subscription_keyendpoint"]

    # Query term(s) to search for.

    # Construct a request
    mkt = "en-US"
    params = {
        "q": word + " " + additional_word,
        "mkt": mkt,
        "freshness": return_period(nws="bing", time_op=time_op),
        # "since": time1,
        "count": 100,
        "sortBy": "Date",
    }
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}

    # Call the API
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as ex:
        return ex


def extract_bing_news(searchword_list, time_op, additional_word):
    bingnewsdf = pd.DataFrame()
    try:
        for wd in searchword_list:
            content = get_bing_news(
                word=wd, time_op=time_op, additional_word=additional_word
            )
            temp_df = pd.DataFrame(content["value"])
            temp_df["searchword"] = wd + " " + additional_word
            temp_df["source"] = temp_df["name"]
            temp_df["link"] = temp_df["url"]
            bingnewsdf = pd.concat([bingnewsdf, temp_df])

            bingnewsdf["exclude"] = bingnewsdf["link"].apply(exclude_site)
            bingnewsdf = bingnewsdf[bingnewsdf["exclude"] == True]

            print(bingnewsdf)

            return bingnewsdf[["searchword", "source", "link", "description", "datePublished"]].to_dict(orient="records")

    except:
        pass#bingnewsdf[["searchword", "source", "link", "description", "datePublished"]].to_dict(orient="records")



def search_bing_news(state):
    """retrieve docs from bing news"""

    #Search
    search_docs = extract_bing_news(searchword_list=[state['question']], time_op=state["time_op"], additional_word="")
    

    #Format
    #try:
    formatted_search_docs = "\n\n---\n\n".join(
            [
            f'<Document source="{doc["source"]}" date="{doc["datePublished"]}"/>\n{doc["source"]}\n{doc["link"]}\n</Document>'
            for doc in search_docs 
            ]
        )

    with st.expander("BingNews取得データ"):
        st.write(formatted_search_docs,key="bingnews")

    return {"context": [formatted_search_docs]} 
    #except:
    #    return {"context": ["-"]} 
