import requests
import json
import streamlit as st
from utils.utils import return_period


def search_youcom(state):
    
    """ Retrieve docs from youcom news search """

    
    try:    
        url = "https://api.ydc-index.io/news"

        querystring = {"query":state['question'],"recency": return_period(nws="youcom", time_op=state["time_op"])}
        #"recency": "month",  # day, week, month, year

        YOUCOM_API_KEY = st.secrets["YOUCOM_API_KEY"]

        headers = {"X-API-Key": YOUCOM_API_KEY}


       # Search
        response = requests.request("GET", url, headers=headers, params=querystring)
        res = json.loads(response.text)

        


        # Format
        formatted_search_docs = "\n\n---\n\n".join(
            [
            f'<Document source="{doc["source_name"]}" date="{doc["page_age"]}"/>\n{doc["title"]}\n{doc["url"]}\n</Document>'
            for doc in res["news"]["results"]
            ])
        #print(formatted_search_docs)
     

        return {"context": [formatted_search_docs]} 
    except:
        return {"context": ["-"]}







