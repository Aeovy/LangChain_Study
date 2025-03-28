from openai import OpenAI
from langchain_tools import tools
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain.schema import HumanMessage, AIMessage
from langchain_core.messages import ToolMessage,HumanMessage
from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser

# 加载.env文件中的环境变量
load_dotenv()

# 从环境变量中获取API密钥和其他配置
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("MODEL_NAME")
base_url = os.getenv("BASE_URL")

# QWEN API
# llm = ChatOpenAI(
#     model_name=model_name,
#     base_url=base_url,
#     api_key=api_key,
#     temperature=0.7,
# )
# OLLAMA API
llm = ChatOpenAI(
    model_name=os.getenv("OLLAMA_MODEL"),
    api_key=os.getenv("OLLAMA_API_KEY"),
    base_url=os.getenv("OLLAMA_BASE_URL"),
    temperature=0.7,
)

# 绑定工具
llm = llm.bind_tools(tools)
input_msg="现在几点了？"




message=[HumanMessage(content=input_msg)]
first=True
for chunk in llm.stream(input_msg):
    print(chunk.content)
    #print("toolcalls",chunk.tool_calls,end="\n")
    if first:
        gathered = chunk
        first = False
    else:
        gathered = gathered + chunk

    #print(gathered.tool_call_chunks)
    #print(gathered.tool_calls)
