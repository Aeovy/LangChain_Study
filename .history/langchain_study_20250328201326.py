from openai import OpenAI
from langchain_tools import tools
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain.schema import HumanMessage, AIMessage
from langchain_core.messages import ToolMessage,HumanMessage,BaseMessage
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
    temperature=0.9,
)

# 绑定工具
llm = llm.bind_tools(tools)
input_msg="告诉我现在的时间，并计算1+2的结果。"




message=[HumanMessage(content=input_msg)]
first=True

aimsg=None
aimsg_toolcall=None
for chunk in llm.stream(input_msg):
    if aimsg is None:
        aimsg=chunk
    else:
        aimsg=aimsg+chunk
    if chunk.content is not None:
        print(chunk.content,end="")
        #return content
    
    if chunk.tool_calls is not None:
        if first:
            aimsg_toolcall = chunk
            first = False
        else:
            aimsg_toolcall = aimsg_toolcall + chunk
        print("toolcalls",chunk.tool_calls,end="\n")
#print(aimsg)
#message.append(aimsg)
