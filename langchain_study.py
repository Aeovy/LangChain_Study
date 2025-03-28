from openai import OpenAI
from langchain_tools import *
from langchain_openai import ChatOpenAI
llm=ChatOpenAI(
    model_name=model,
    base_url=base_url,
    api_key="sk-f68da0909e0e4790ab6d715f1dc33e84",
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