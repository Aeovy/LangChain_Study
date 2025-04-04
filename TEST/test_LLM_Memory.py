import sys
import os
# 添加上一级目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

llm=ChatOpenAI(
    model_name=os.getenv("OPENAI_MODEL_NAME"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    temperature=0.7,
    max_tokens=4096,
    streaming=True,
)
from langchain_core.messages import HumanMessage,ToolMessage,AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, connection="sqlite:///memory.db")
async def load_memory_async(conversion_id)-> SQLChatMessageHistory:
    async_engine = create_async_engine("sqlite+aiosqlite:///memory.db")
    async_message_history = SQLChatMessageHistory(
    session_id=conversion_id, connection=async_engine,
    )
    return async_message_history
async def main(conversion_id):
    # 使用异步加载记忆对象
    memory_history = await load_memory_async(conversion_id=conversion_id)
    # 使用异步方法获取消息列表
    messages = await memory_history.aget_messages()
    print("Retrieved messages:", messages)
    #print("Memory history:", memory_history)



if __name__=="__main__":
    conversion_id="1"
    asyncio.run(main(conversion_id))

