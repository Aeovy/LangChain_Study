import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage,HumanMessage,AIMessage
from langchain_tools import add,multiply,get_time,tools,tools_dict
from dotenv import load_dotenv
from langchain_community.chat_message_histories import ChatMessageHistory
class LLM_Model():
    def __init__(self, model_type: str="ollama",temperature: float=0.9,tools: list=None,tools_dict: dict=None,maxtoken=2048):
        load_dotenv()
        if model_type.lower()=="openai":
            self.__api_key = os.getenv("OPENAI_API_KEY")
            self.model_name = os.getenv("MODEL_NAME")
            self.base_url = os.getenv("BASE_URL")
        elif model_type.lower()=="ollama":
            self.__api_key = os.getenv("OLLAMA_API_KEY")
            self.model_name = os.getenv("OLLAMA_MODEL")
            self.base_url = os.getenv("OLLAMA_BASE_URL")
        elif model_type.lower()=="lmstudio":
            self.__api_key = os.getenv("LMSTUDIO_API_KEY")
            self.model_name = os.getenv("LMSTUDIO_MODEL")
            self.base_url = os.getenv("LMSTUDIO_BASE_URL")
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
        self.Chat_Memory=ChatMessageHistory()

    def load_memory():
        #load Json
        pass
    def reduce_memory_used_space(Memory:ChatMessageHistory):
        # 用LLM总结聊天上下文
        pass
    def bindtools(self,tools: list, tools_dict: dict):
        if tools!=None and tools_dict!=None:
            self.tools=tools
            self.tools_dict=tools_dict
            self.LLM = self.LLM.bind_tools(tools)
    def chat(self, qurey:str):
        message=[HumanMessage(qurey)]
        Is_chat_finished=True
        aimsg=None
        while True:
            Is_chat_finished=True
            for chunk in self.LLM.stream(message):
                print(chunk)
                ############
                if aimsg is None:
                    aimsg=chunk
                else:
                    aimsg=aimsg+chunk
                ############
                if chunk.content!="":
                    #print(chunk.content,end="")
                    #return content
                    pass
            print("\n")
            message.append(aimsg)
            if aimsg.tool_calls:
                Is_chat_finished=False
                tools_result=self.function_call(aimsg)
                print("tools:",tools_result)
                message.append(tools_result)
                #message.append(self.function_call(aimsg))            
            aimsg=None       
            if Is_chat_finished==True:
                print("\n")
                #return XXXX
                break
            print("all message:",message)
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
class LLM_Model_async(LLM_Model):
    def __init__(self, model_type: str="ollama",temperature: float=0.9,tools: list=tools,tools_dict: dict=tools_dict):
        super().__init__(model_type=model_type,temperature=temperature,tools=tools,tools_dict=tools_dict)

    async def chat_async(self, qurey):####message预定为当前对话上下文
        if type(qurey)==str:
            self.Chat_Memory.add_user_message(qurey)
            message=[HumanMessage(qurey)]
        else:#当使用function call后，会递归该函数，此时input的qurey的type为list
            message=qurey
        chunks=None
        async for chunk in self.LLM.astream(message):
            #print("chunk:",chunk)
            if chunks is None:
                chunks=chunk
            else:
                chunks=chunks+chunk
            # 正常传输内容时，直接输出LLM的content###############
            if chunk.content!="":
                #print(chunk.content,end="",flush=True)
                pass
            ###################################################
        #print("chunks",chunks)
        if chunks.response_metadata.get("finish_reason","")!="":
            message.append(chunks)
            print("Chunks:",chunks)
            print("message:",message)
            Have_toolcalls=len(chunks.tool_calls)>0
            if chunks.response_metadata["finish_reason"]=="stop" and Have_toolcalls==False:
                #save memory
                
                pass
            # 有的模型调用function call时，stop reason不一定为"tool_calls"
            elif chunks.response_metadata["finish_reason"]=="tool_calls" or Have_toolcalls==True: 
                
                function_call_result=self.function_call(chunks)
                for function_msg in function_call_result:
                    message.append(function_msg)
                task=asyncio.create_task(self.chat_async(message))
                await task 
            else:
                #print("debug_status:",chunks)
                pass
       

            
        
            

from langchain_tools import tools, tools_dict
async def main():
    test_model=LLM_Model_async(model_type="openai",temperature=0.6,tools=tools,tools_dict=tools_dict)
    qurey="计算123+456和123X456的结果"

    task1=asyncio.create_task(test_model.chat_async(qurey))
    await task1
if __name__ == "__main__":
    asyncio.run(main())