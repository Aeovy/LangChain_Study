from openai import OpenAI
from langchain_tools import tools  # 只导入tools，不再导入model和base_url
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# 加载.env文件中的环境变量
load_dotenv()

# 从环境变量中获取API密钥和其他配置
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")  # 提供默认值
base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")  # 提供默认值

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

#aimsg=llm.invoke(input_msg)
#print(aimsg)
#print(aimsg.tool_calls)

for chunk in llm.stream(input_msg):
    print(chunk.content,end="")
#     print(chunk.tool_calls)
#     content.append(chunk.content)
#     tool_msg.append(chunk.tool_calls)