from openai import OpenAI
from langchain_tools import tools  
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# 加载.env文件中的环境变量
load_dotenv()

# 从环境变量中获取API密钥和其他配置
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("MODEL_NAME")  
base_url = os.getenv("BASE_URL")

llm=ChatOpenAI(
    model_name=model_name,
    base_url=base_url,
    api_key=api_key,
    temperature=0.7,
)
llm=llm.bind_tools(tools)
input_msg="现在几点了"
content=[]
tool_msg=[]

print(llm.invoke(input_msg).too


# for chunk in llm.stream(input_msg):
#     print(chunk.content,end="")
#     print(chunk.tool_calls)
#     content.append(chunk.content)
#     tool_msg.append(chunk.tool_calls)