import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage,HumanMessage,AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_tools import tools,tools_dict
from dotenv import load_dotenv
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from sqlalchemy.ext.asyncio import create_async_engine
class LLM_Model():
    def __init__(self, model_type: str="ollama",temperature: float=0.6,tools: list=None,tools_dict: dict=None,maxtoken=2048):
        load_dotenv()
        self.__api_key = os.getenv(f"{model_type.upper()}_API_KEY")
        self.model_name = os.getenv(f"{model_type.upper()}_MODEL_NAME")
        self.base_url = os.getenv(f"{model_type.upper()}_BASE_URL")
        self.LLM=ChatOpenAI(
            model_name=self.model_name,
            api_key=self.__api_key,
            base_url=self.base_url,
            temperature=temperature,
            max_tokens=maxtoken,
            streaming=True,
        )
        
        self.bindtools(tools, tools_dict)
        
         ####加入对话记忆####
        
        
        # self.LLM=RunnableWithMessageHistory(
        #     self.LLM,
        #     self.load_memory,
        #     )
        

    def load_memory(self,conversion_id)-> SQLChatMessageHistory:
        return SQLChatMessageHistory(conversion_id, connection="sqlite:///memory.db")
    
    async def load_memory_async(self,conversion_id)-> SQLChatMessageHistory:
        async_engine = create_async_engine("sqlite+aiosqlite:///memory.db")
        async_message_history = SQLChatMessageHistory(
        session_id=conversion_id, connection=async_engine,
        )
        return async_message_history
    def summary_memory(self):
        # 用LLM总结聊天上下文
        pass
    def bindtools(self,tools: list, tools_dict: dict):
        if tools!=None and tools_dict!=None:
            self.tools=tools
            self.tools_dict=tools_dict
            self.LLM = self.LLM.bind_tools(tools)
    
    async def chat_async(self, qurey:str=None,Conversion_ID:str=None):
        self.LLM_async=RunnableWithMessageHistory(
            self.LLM,
            self.load_memory_async,
            )
        chat_history=await self.load_memory_async(Conversion_ID)
        
        if qurey is not None:
            await chat_history.aadd_message(HumanMessage(content=qurey))
        chunks=None
        async for chunk in self.LLM_async.astream(chat_history,config={"configurable": {"session_id": Conversion_ID}}):
            #print("chunk:",chunk)
            if chunks is None:
                chunks=chunk
            else:
                chunks=chunks+chunk
            # 正常传输内容时，直接输出LLM的content###############
            if chunk.content!="":
                print(chunk.content,end="",flush=True)
                pass
            ###################################################
        #print("chunks",chunks)
        if chunks.response_metadata.get("finish_reason","")!="":
            print("Chunks:",chunks)
            Have_toolcalls=len(chunks.tool_calls)>0
            if chunks.response_metadata["finish_reason"]=="stop" and Have_toolcalls==False:
                #save memory
                
                pass
            # 有的模型调用function call时，stop reason不一定为"tool_calls"
            elif chunks.response_metadata["finish_reason"]=="tool_calls" or Have_toolcalls==True: 
                
                function_call_result=self.function_call(chunks)
                for function_msg in function_call_result:
                    chat_history.add_message(function_msg)
                task=asyncio.create_task(self.chat_async(None,Conversion_ID))
                await task 
            else:
                #print("debug_status:",chunks)
                pass
         
    def function_call(self,aimsg):
        result=[]
        for tool_calls in aimsg.tool_calls:
                try:   
                ###############Use tools#############
                    #print("test",tool_calls["name"])
                    selected_tool = self.tools_dict[tool_calls["name"].lower()]
                    #tool_output =tool_calls["name"].lower()+" result:"+ str(selected_tool.invoke(tool_calls["args"]))
                    tool_output = selected_tool.invoke(tool_calls)
                    result.append(tool_output) 
                #####################################
                except Exception as e:
                    result.append(ToolMessage(e))
        return result

import asyncio
#tesst
from langchain_tools import tools, tools_dict
async def main():
    test_model=LLM_Model(model_type="openai",temperature=0.6,tools=tools,tools_dict=tools_dict)
    qurey="计算123+456和123X456的结果"
    task1=asyncio.create_task(test_model.chat_async(qurey,"1"))
    await task1
if __name__ == "__main__":
    asyncio.run(main())