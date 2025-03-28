from openai import OpenAI
from langchain_tools import tools, add, multiply, get_time
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
llm = ChatOpenAI(
    model_name=model_name,
    base_url=base_url,
    api_key=api_key,
    temperature=0.7,
)
# OLLAMA API
# llm = ChatOpenAI(
#     model_name=os.getenv("OLLAMA_MODEL"),
#     api_key=os.getenv("OLLAMA_API_KEY"),
#     base_url=os.getenv("OLLAMA_BASE_URL"),
#     temperature=0.9,
# )

# 绑定工具
llm = llm.bind_tools(tools)
input_msg="告诉我现在的时间，并计算100+300的结果。"




message=[HumanMessage(input_msg)]



#chat with model
##############################
Is_chat_finished=True
Is_tools_Used=False
first=True
aimsg=None
aimsg_toolcall=None
while True:
    Is_chat_finished=True
    #待改成异步
    for chunk in llm.stream(message):
        ############
        if aimsg is None:
            aimsg=chunk
        else:
            aimsg=aimsg+chunk
        ############
        if chunk.content is not None:
            print(chunk.content,end="")
            #or return content
            pass
        if aimsg
        ###############Use tools#############
        Is_tools_Used=True
        Is_chat_finished=False
        selected_tool = {"add": add, "multiply": multiply,"get_time":get_time}[chunk.tool_calls[0]["name"].lower()]
        tool_output = selected_tool.invoke(chunk.tool_calls[0]["args"])
        message.append(ToolMessage(tool_output, tool_call_id=chunk.tool_calls[0]["id"]))
        #####################################
    message.append(aimsg)
    #print(aimsg)
    aimsg=None       
        
    #print(message)
    if Is_chat_finished:
        break
###############################

