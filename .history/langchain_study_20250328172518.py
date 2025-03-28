from openai import OpenAI
from langchain_tools import *
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# 加载.env文件中的环境变量
load_dotenv()

# 从环境变量中获取API密钥
api_key = os.getenv("OPENAI_API_KEY")

llm=ChatOpenAI(
    model_name=model,
    base_url=base_url,
    api_key=api_key,  # 使用从.env文件中读取的API密钥
    temperature=0.7,
)
llm=llm.bind_tools(tools)
input_msg="现在几点了"
content=[]
tool_msg=[]

#aimsg=llm.invoke(input_msg)
#print(aimsg)
#print(aimsg.tool_calls)

for chunk in llm.stream(input_msg):
    print(chunk.content,end="")
#     print(chunk.tool_calls)
#     content.append(chunk.content)
#     tool_msg.append(chunk.tool_calls)