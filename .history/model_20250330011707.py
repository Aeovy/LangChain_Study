import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage,HumanMessage,AIMessage
from langchain_tools import add,multiply,get_time,tools,tools_dict
from dotenv import load_dotenv
class LLM_Model():
    def __init__(self, model_type: str="ollama",temperature: float=0.9,tools: list=None,tools_dict: dict=None,maxtoken=8192):
        load_dotenv()
        if model_type.lower()=="openai":
            self.__api_key = os.getenv("OPENAI_API_KEY")
            self.model_name = os.getenv("MODEL_NAME")
            self.base_url = os.getenv("BASE_URL")
        elif model_type.lower()=="ollama":
            self.__api_key = os.getenv("OLLAMA_API_KEY")
            self.model_name = os.getenv("OLLAMA_MODEL")
            self.base_url = os.getenv("OLLAMA_BASE_URL")
        self.LLM=ChatOpenAI(
            model_name=self.model_name,
            api_key=self.__api_key,
            base_url=self.base_url,
            temperature=temperature,
            max_tokens=maxtoken,
            streaming=True,
        )
        
        self.bindtools(tools, tools_dict)
            
        self.history_message =None
        ####未来加入读取历史消息的功能####
        #self.history_message = self.read_history_message()
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
        for tool_calls in aimsg.tool_calls:
            ###############Use tools#############
                #print("test",tool_calls["name"])
                selected_tool = self.tools_dict[tool_calls["name"].lower()]
                tool_output =tool_calls["name"].lower()+" result:"+ str(selected_tool.invoke(tool_calls["args"]))
                return ToolMessage(tool_output, tool_call_id=tool_calls["id"])
            #####################################

import asyncio
#tesst
class LLM_Model_async(LLM_Model):
    def __init__(self, model_type: str="ollama",temperature: float=0.9,tools: list=tools,tools_dict: dict=tools_dict):
        super().__init__(model_type=model_type,temperature=temperature,tools=tools,tools_dict=tools_dict)

    async def chat_async(self, qurey):####message预定为全部上下文
        if type(qurey)==str:
            message=[HumanMessage(qurey)]
        else:
            message=qurey
        AI_MSGS_content=""
        chunks=None
        async for chunk in self.LLM.astream(message):
            print("chunk:",chunk)
            if chunks is None:
                chunks=chunk
            else:
                chunks=chunks+chunk
            # 正常传输内容时，直接输出LLM的content###############
            if chunk.content!="":
                #print(chunk.content,end="")
                AI_MSGS_content+=chunk.content
            ###################################################
        #print("temp_msg:",message)
        if chunks.response_metadata.get("finish_reason","")!="":
            message.append(AIMessage(AI_MSGS_content))
            if chunks.response_metadata["finish_reason"]=="stop":
                pass
            elif chunks.response_metadata["finish_reason"]=="tool_calls":
                function_call_result=self.function_call(chunks)
                message.append(function_call_result)
                task=asyncio.create_task(self.chat_async(message))
                await task 
            else:
                pass
        ##memory管理
        #print("test",AI_MSGS_content)
        #print(chunks)
        #print(message)
            
        
            
async def test_async():
    print("test_async")


from langchain_tools import tools, tools_dict
async def main():
    test_model=LLM_Model_async(model_type="openai",temperature=0.7,tools=tools,tools_dict=tools_dict)
    qurey="现在几点了"
    task1=asyncio.create_task(test_model.chat_async(qurey))
    await task1
if __name__ == "__main__":
    asyncio.run(main())