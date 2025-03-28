from openai import OpenAI
from langchain_tools import tools
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain.schema import HumanMessage, AIMessage
from langchain_core.messages import ToolMessage
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

# output=llm.invoke("现在几点了？")
# # 解析工具的输出
# print(output)
# print(output.tool_calls)
temp=None
async for chunk in llm.stream("现在几点了？"):
    #print("chunk:",chunk,end="\n")
    print("toolcalls",chunk.tool_calls,end="\n")
    #temp=temp+chunk.tool_calls