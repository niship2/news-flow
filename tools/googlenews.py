from utils.utils import utils
import pandas as pd
import requests
import streamlit as st
import datetime
from datetime import datetime
from serpapi import GoogleSearch


SERPAPI_API_KEY = st.secrets['SERP_API_KEY']

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



def extract_google_news_json(searchword_list, time_op, additional_word):
    time = return_period(nws="google", time_op=time_op)

    serp_url_list = []
    wds = []
    words = searchword_list
    for wd in words:
        params = {
            "api_key": SERPAPI_API_KEY,
            "engine": "google",
            "q": wd + " " + additional_word,
            "google_domain": "google.com",
            # "hl": "en",
            "filter": 1,
            "tbm": "nws",
            "sbd":1,
            "as_qdr": time,
            "num": 100,
            
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        # urlを抽出
        import requests

        # serp_url_list.append(results["search_information"]["menu_items"][0]["serpapi_link"])
        serp_url_list.append(results["search_metadata"]["json_endpoint"])
        wds.append(wd)
        try:
            for res in results["serpapi_pagination"]["other_pages"].values():
                jsonres = requests.get(res + "&api_key=" + SERPAPI_API_KEY)
                # print(jsonres.json()["search_metadata"]["json_endpoint"])
                serp_url_list.append(jsonres.json()["search_metadata"]["json_endpoint"])
                wds.append(wd)
        except:
            pass

    gnews_df = pd.DataFrame()
    for url in serp_url_list:
        r = requests.get(url)  # +"&api_key=" + serp_api_key)
        res = r.json()

        try:
            temp_df = pd.DataFrame(res["news_results"])
            temp_df["searchword"] = res["search_information"]["query_displayed"]
            gnews_df = pd.concat([gnews_df, temp_df])
        except:
            pass

    # ちょっと整形
    #gnews_df = gnews_df.reset_index().drop(
    #    columns={"position", "index"}
    #)  # ["pubdate","url","title","description","related_industries","related_companies","keywords"]
    gnews_df["date"] = gnews_df["date"].apply(get_date_format)
    gnews_df["exclude"] = gnews_df["link"].apply(exclude_site)
    gnews_df = gnews_df[gnews_df["exclude"] == True]
    # gnews_df["genre"] = task_name

    return gnews_df[["searchword", "title", "link", "date", "source", "snippet"]].to_dict(orient="records")



def extract_google_news_JA_json(searchword_list, time_op, additional_word):
    time = return_period(nws="google", time_op=time_op)

    serp_url_list = []
    wds = []
    additional_word = ""
    words = searchword_list
    for wd in words:
        params = {
            "api_key": SERPAPI_API_KEY,
            "engine": "google",
            "q": wd + " " + additional_word,
            "google_domain": "google.co.jp",
            #"hl": "ja",
            #"gl":"ja",
            "gl":"JP",
            "filter": 1,
            "tbm": "nws",
            "sbd":1,
            "as_qdr": time,
            "num": 100,
        }
        search = GoogleSearch(params)
        results = search.get_dict()


        # urlを抽出
        import requests

        # serp_url_list.append(results["search_information"]["menu_items"][0]["serpapi_link"])
        serp_url_list.append(results["search_metadata"]["json_endpoint"])
        wds.append(wd)
        try:
            for res in results["serpapi_pagination"]["other_pages"].values():
                jsonres = requests.get(res + "&api_key=" + SERPAPI_API_KEY)
                # print(jsonres.json()["search_metadata"]["json_endpoint"])
                serp_url_list.append(jsonres.json()["search_metadata"]["json_endpoint"])
                wds.append(wd)
        except:
            pass

    gnews_df = pd.DataFrame()
    for url in serp_url_list:
        r = requests.get(url)  # +"&api_key=" + serp_api_key)
        res = r.json()

        try:
            temp_df = pd.DataFrame(res["news_results"])
            temp_df["searchword"] = res["search_information"]["query_displayed"]
            gnews_df = pd.concat([gnews_df, temp_df])
        except:
            pass

    # ちょっと整形
    #gnews_df = gnews_df.reset_index().drop(
    #    columns={"position", "index"}
    #)  # ["pubdate","url","title","description","related_industries","related_companies","keywords"]
    gnews_df["date"] = gnews_df["date"].apply(get_date_format)
    gnews_df["exclude"] = gnews_df["link"].apply(exclude_site)
    gnews_df = gnews_df[gnews_df["exclude"] == True]
    # gnews_df["genre"] = task_name

    return gnews_df[["searchword", "title", "link", "date", "source", "snippet"]].to_dict(orient="records")




def search_google_news(state):
    """retrieve docs from google news"""

    try:
        
        #Search
        search_docs = extract_google_news_json(searchword_list=[state['question']], time_op="直近1ヶ月", additional_word="")

        #Format
        formatted_search_docs = "\n\n---\n\n".join(
            [
            f'<Document source="{doc["source"]}" date="{doc["date"]}"/>\n{doc["title"]}\n{doc["link"]}\n</Document>'
            for doc in search_docs
            ])
    
        #print(formatted_search_docs)
        with st.expander("GoogleNews取得データ"):
            st.write(formatted_search_docs)        


        return {"context": [formatted_search_docs]} 
    except:
        st.write("GoogleNews取得失敗")
        return {"context": ["-"]}


def search_google_news_JA(state):
    """retrieve docs from google news"""

    try:
        #Search
        search_docs_JA = extract_google_news_JA_json(searchword_list=[state['question']], time_op="直近1ヶ月", additional_word="")

        #Format
        formatted_search_docs_JA = "\n\n---\n\n".join(
            [
            f'<Document source="{doc["source"]}" date="{doc["date"]}"/>\n{doc["title"]}\n{doc["link"]}\n</Document>'
            for doc in search_docs_JA
            ])
    
        #print(formatted_search_docs)

        with st.expander("GoogleNews_JA取得データ"):
            st.write(formatted_search_docs_JA)


        return {"context": [formatted_search_docs_JA]}    
    except:
        st.write("GoogleNews_JA取得失敗")
        return {"context": ["-"]}
