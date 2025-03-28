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

message = [HumanMessage(input_msg)]
Is_chat_finished = True

while True:
    response_content = ""
    aimsg = None
    Is_chat_finished = True
    
    for chunk in llm.stream(message):
        if chunk.content is not None:
            response_content += chunk.content
            print(chunk.content, end="")
        
        # 正确处理消息累积
        if aimsg is None:
            aimsg = chunk
        else:
            aimsg = aimsg + chunk
            
        # 处理工具调用
        if chunk.tool_calls and len(chunk.tool_calls) > 0:
            Is_chat_finished = False
            break  # 一旦发现工具调用，暂停处理其余块
    
    # 如果检测到工具调用，处理工具调用
    if not Is_chat_finished and aimsg.tool_calls:
        # 处理所有工具调用
        for tool_call in aimsg.tool_calls:
            try:
                tool_name = tool_call["name"].lower()
                if tool_name in ["add", "multiply", "get_time"]:
                    selected_tool = {"add": add, "multiply": multiply, "get_time": get_time}[tool_name]
                    tool_output = selected_tool.invoke(tool_call["args"])
                    message.append(aimsg)  # 添加AI消息
                    message.append(ToolMessage(content=tool_output, tool_call_id=tool_call["id"]))
            except Exception as e:
                print(f"工具调用出错: {e}")
    else:
        # 如果没有工具调用，添加AI消息并退出循环
        message.append(aimsg)
        break

print("\n对话完成")

