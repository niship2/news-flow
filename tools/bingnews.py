from utils.utils import utils
import streamlit as st
import pandas as pd
import requests
import datetime
from datetime import datetime


def get_date_format(d):
    dt = datetime.today()  # ローカルな現在の日付と時刻を取得
    if "hours ago" in str(d) or "mins ago" in str(d):
        return dt.date()
    else:
        return str(d)


def return_period(nws, time_op):
    if nws == "google":
        if time_op == "直近24時間":
            return "d1"
        elif time_op == "直近1週間":
            return "w1"
        elif time_op == "直近2週間":
            return "w2"
        elif time_op == "直近1ヶ月":
            return "m1"
        elif time_op == "過去1年":
            return "1y"
        else:
            return "d1"
    else:
        if time_op == "直近24時間":
            return "Day"
        elif time_op == "直近1週間":
            return "Week"
        elif time_op == "直近2週間":
            return "Week"
        elif time_op == "直近1ヶ月":
            return "Month"
        else:
            return "Day"


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
            bingnewsdf = get_bing_news[bingnewsdf["exclude"] == True]

            return bingnewsdf[["searchword", "source", "link", "description", "datePublished"]].to_dict(orient="records")

    except:
        pass#bingnewsdf[["searchword", "source", "link", "description", "datePublished"]].to_dict(orient="records")


@st.cache_data
def search_bing_news(state):
    """retrieve docs from bing news"""

    #Search
    search_docs = extract_bing_news(searchword_list=[state['question']], time_op="直近2週間", additional_word="")

    #Format
    try:
        formatted_search_docs = "\n\n---\n\n".join(
            [
            f'<Document source="{doc["source"]}" date="{doc["datePublished"]}"/>\n{doc["source"]}\n{doc["link"]}\n</Document>'
            for doc in search_docs 
            ]
        )

        with st.expander("BingNews取得データ"):
            st.write(formatted_search_docs)

        return {"context": [formatted_search_docs]} 
    except:
        return {"context": ["-"]} 
