import pandas as pd
import requests
import streamlit as st
import datetime
from datetime import datetime, timedelta
from serpapi import GoogleSearch
from utils.utils import return_period


SERPAPI_API_KEY = st.secrets['SERP_API_KEY']




def get_date_format(d):
    dt = datetime.today()  # ローカルな現在の日付と時刻を取得
    if "hours ago" in str(d) or "mins ago" in str(d) or "hour ago" in str(d) or "min ago" in str(d):
        ago = dt.date()
    elif "days ago" in str(d):
        ago =dt.date() - timedelta(days=int(d.replace(" days ago", "")))
    elif "day ago" in str(d):
        ago = dt.date() - timedelta(days=int(d.replace(" day ago", "")))        
    elif "weeks ago" in str(d):
        ago = dt.date() - timedelta(weeks=int(d.replace(" weeks ago", "")))
    elif "week ago" in str(d):
        ago = dt.date() - timedelta(weeks=int(d.replace(" week ago", "")))
    elif "時間前" in str(d) or "分前" in str(d):
        ago = dt.date()
    elif "日前" in str(d):
        ago = dt.date() - timedelta(days=int(d.replace("日前", "")))
    elif "週間前" in str(d):
        ago = dt.date() - timedelta(weeks=int(d.replace("週間前", "")))
    else:
        ago= dt.date()

    print(str(ago))

    return str(ago)[0:10]



def exclude_site(url):
    #if "yahoo" in url:
    #    return False
    #else:
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
        #try:
        #    for res in results["serpapi_pagination"]["other_pages"].values():
        #        jsonres = requests.get(res + "&api_key=" + SERPAPI_API_KEY)
        #        # print(jsonres.json()["search_metadata"]["json_endpoint"])
        #        serp_url_list.append(jsonres.json()["search_metadata"]["json_endpoint"])
        #        wds.append(wd)
        #except:
        #    pass

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
        #try:
        #  残りのヒット分も全部取る場合
        #    for res in results["serpapi_pagination"]["other_pages"].values():
        #        jsonres = requests.get(res + "&api_key=" + SERPAPI_API_KEY)
        #        # print(jsonres.json()["search_metadata"]["json_endpoint"])
        #        serp_url_list.append(jsonres.json()["search_metadata"]["json_endpoint"])
        #        wds.append(wd)
        #except:
        #    pass

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
    gnews_df["date"] = gnews_df["date"].apply(get_date_format)
    gnews_df["exclude"] = gnews_df["link"].apply(exclude_site)
    gnews_df = gnews_df[gnews_df["exclude"] == True]
    
    return gnews_df[["searchword", "title", "link", "date", "source", "snippet"]].to_dict(orient="records")




def search_google_news(state):
    """retrieve docs from google news"""

    try:
        
        #Search
        search_docs = extract_google_news_json(searchword_list=[state['question']], time_op=state["time_op"], additional_word="")

        #Format
        formatted_search_docs = "\n\n---\n\n".join(
            [
            f'<Document source="{doc["source"]}" date="{doc["date"]}"/>\n{doc["title"]}\n{doc["link"]}\n</Document>'
            for doc in search_docs
            ])
    


        return {"context": [formatted_search_docs]} 
    except:
        st.write("GoogleNews取得失敗")
        return {"context": ["-"]}


def search_google_news_JA(state):
    """retrieve docs from google news"""

    try:
        #Search
        search_docs_JA = extract_google_news_JA_json(searchword_list=[state['question']], time_op=state["time_op"], additional_word="")

        #Format
        formatted_search_docs_JA = "\n\n---\n\n".join(
            [
            f'<Document source="{doc["source"]}" date="{doc["date"]}"/>\n{doc["title"]}\n{doc["link"]}\n</Document>'
            for doc in search_docs_JA
            ])
    
        #print(formatted_search_docs)


        return {"context": [formatted_search_docs_JA]}    
    except Exception as e:
        print(e)
        st.write("GoogleNews_JA取得失敗")
        return {"context": ["-"]}
