def utils():
    os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
    os.environ['TAVILY_API_KEY'] = st.secrets['TAVILY_API_KEY']
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

    from typing import List,Dict
    from langchain_core.messages import HumanMessage
    from langgraph.graph import END, MessageGraph

    from langchain.output_parsers import (
        RetryWithErrorOutputParser,
        PydanticOutputParser,
    )

    from langchain.prompts import PromptTemplate
    from langchain_core.pydantic_v1 import BaseModel, Field, validator

    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_openai import ChatOpenAI

    #from IPython.display import Image, display

    from typing import Any
    from typing_extensions import TypedDict

    from langgraph.graph import StateGraph, START, END


    from typing import List,Dict

