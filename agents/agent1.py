import streamlit as st
from typing import List,Dict
from langchain_core.messages import HumanMessage
from langgraph.graph import END, MessageGraph
from langchain.output_parsers import (
    RetryWithErrorOutputParser,
    PydanticOutputParser,
)

from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator

#from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

#from IPython.display import Image, display

from typing import Any
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END



#@title stateとか定義
import operator
from typing import Annotated
from datetime import date, datetime, time, timedelta

#@title agent
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOpenAI(model="gpt-4o",temperature=0.2)

from tools.bingnews import search_bing_news
from tools.googlenews import search_google_news_JA
from tools.googlenews import search_google_news
from tools.tavilysearch import search_tavily
from tools.wikipedia import search_wikipedia
from tools.youcom import search_youcom


class State(TypedDict):
    question: str
    answer: str
    context: Annotated[list, operator.add]
    time_op: str


class FinalAnswer(BaseModel):
    title:str
    date: datetime
    source_url:str
    japanese_translation:str

    def formatted_date(self):
        return self.date.strftime('%Y-%m-%d')
  

class FinalAnswers(BaseModel):
    content:list[FinalAnswer]  



def generate_answer(state):
    
    """ Node to answer a question """

    # Get state
    context = state["context"]
    question = state["question"]

    # Template
    answer_template = """list the articles using this context: {context}"""
    answer_instructions = answer_template.format(question=question, 
                                                       context=context)    
    
    # Answer
    try:
        answer = llm.with_structured_output(FinalAnswers).invoke([SystemMessage(content=answer_instructions)]+[HumanMessage(content=f"List the articles")])
    except:
        answer_instructions = answer_template.format(question=question, 
                                                       context=context[0:10000])
        answer = llm.with_structured_output(FinalAnswers).invoke([SystemMessage(content=answer_instructions)]+[HumanMessage(content=f"List the articles")])
            

      
    # Append it to state
    return {"answer": answer}


def remove_duplicate(state):
    """ Node to remove duplicate article"""

    #Get State
    context = state["context"]
    question = state["question"]
    answer = state["answer"]

    #print(answer)

    # Template
    answer_template = """
    * Combine similar or duplicate articles based on the title and date of the article.
    * Also removedelete articles not related to technology,startups, fundraising, talent acquisition, mergers and acquisitions or IPOs. 
    \n\n articles of this answer: {answer}"""
    answer_instructions = answer_template.format(answer=answer)    
    ##
    # Answer

    answer = llm.with_structured_output(FinalAnswers).invoke([SystemMessage(content=answer_instructions)]+[HumanMessage(content=f"Remove duplicates.")])
      
    # Append it to state
    return {"answer": answer}    




def agent_builder(select_tools):
    # Add nodes
    builder = StateGraph(State)

    #select_tools = ["search_google_news","search_google_news_JA","search_bing_news"]
    #,"search_wikipedia","search_tavily"

    if "search_tavily" in select_tools:
        builder.add_node("search_tavily", search_tavily)
        builder.add_edge(START, "search_tavily")
        builder.add_edge("search_tavily", "generate_answer")

    if "search_wikipedia" in select_tools:
        builder.add_node("search_wikipedia", search_wikipedia)
        builder.add_edge(START, "search_wikipedia")
        builder.add_edge("search_wikipedia", "generate_answer")

    if "search_google_news" in select_tools:
        builder.add_node("search_google_news", search_google_news)
        builder.add_edge(START, "search_google_news")
        builder.add_edge("search_google_news", "generate_answer")
    
    if "search_google_news_JA" in select_tools:
        builder.add_node("search_google_news_JA", search_google_news_JA)
        builder.add_edge(START, "search_google_news_JA")
        builder.add_edge("search_google_news_JA", "generate_answer")

    if "search_bing_news" in select_tools:
        builder.add_node("search_bing_news", search_bing_news)
        builder.add_edge(START, "search_bing_news")
        builder.add_edge("search_bing_news", "generate_answer")

    if "search_youcom" in select_tools:
        builder.add_node("search_youcom", search_youcom)
        builder.add_edge(START, "search_youcom")
        builder.add_edge("search_youcom", "generate_answer")


    # Initialize each node with node_secret 
    builder.add_node("generate_answer", generate_answer)
    builder.add_node("remove_duplicate", remove_duplicate)

    # 
    builder.add_edge("generate_answer", "remove_duplicate")
    builder.add_edge("remove_duplicate", END)

    graph = builder.compile()

    return graph