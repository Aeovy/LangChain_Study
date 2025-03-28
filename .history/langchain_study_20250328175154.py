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
model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

# 初始化LLM
llm = ChatOpenAI(
    model_name=model_name,
    base_url=base_url,
    api_key=api_key,
    temperature=0.7,
)

# 绑定工具
llm = llm.bind_tools(tools)

# 函数调用示例
def run_function_call():
    # 1. 基本调用 - 直接获取tool_calls
    input_msg = "现在几点了，请告诉我完整时间"
    response = llm.invoke(input_msg)
    
    print("=== 基本工具调用响应 ===")
    print(f"内容: {response.content}")
    print(f"工具调用: {response.tool_calls}")
    
    # 2. 处理工具调用结果
    if response.tool_calls:
        for tool_call in response.tool_calls:
            function_name = tool_call.name
            arguments = tool_call.args
            
            print(f"\n执行工具: {function_name}")
            print(f"参数: {arguments}")
            
            # 根据工具名称调用相应的函数
            for tool in tools:
                if tool.__name__ == function_name:
                    result = tool(**arguments)
                    print(f"工具执行结果: {result}")
                    
                    # 生成包含工具结果的新消息
                    tool_message = ToolMessage(content=str(result), name=function_name)
                    
                    # 继续与LLM对话，提供工具执行结果
                    final_response = llm.invoke([
                        HumanMessage(content=input_msg),
                        AIMessage(content=response.content, tool_calls=response.tool_calls),
                        tool_message
                    ])
                    
                    print("\n=== 最终响应 ===")
                    print(final_response.content)
                    break

# 执行函数调用示例
run_function_call()