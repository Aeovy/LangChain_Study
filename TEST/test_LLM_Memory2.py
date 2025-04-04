import sys
import os
# 添加上一级目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import Annotated
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_tools import tools
from dotenv import load_dotenv
load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)


# tool = TavilySearchResults(max_results=2)
# tools = [tool]
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL_NAME"),
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    temperature=0.7,
    max_tokens=4096,
    streaming=True,
)
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")
graph = graph_builder.compile()
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_tools import add,multiply
test_tool = TavilySearchResults(max_results=2,tavily_api_key="124512424")
test_tools = [test_tool]
print(test_tool)
print(test_tools,type(test_tools))
print(add)
print([add],type([add]))
#print(tools)