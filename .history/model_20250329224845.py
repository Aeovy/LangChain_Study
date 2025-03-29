import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage,HumanMessage
from langchain_tools import add,multiply,get_time,tools,tools_dict
from dotenv import load_dotenv
class LLM_Model():
    def __init__(self, model_type: str="ollama",temperature: float=0.9,tools: list=None,tools_dict: dict=None):
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
        )
        self.tools=tools
        self.tools_dict=tools_dict
        self.bindtools(tools, tools_dict)
            
        self.history_message =None
        ####未来加入读取历史消息的功能####
        #self.history_message = self.read_history_message()
    def bindtools(self,tools: list, tools_dict: dict):
        if tools:
            self.LLM = self.LLM.bind_tools(tools)
            if tools_dict:
                self.tools_dict = tools_dict
    def chat(self, qurey:str):
        message=[HumanMessage(qurey)]
        Is_chat_finished=True
        aimsg=None
        while True:
            Is_chat_finished=True
            for chunk in self.LLM.stream(message):
                ############
                if aimsg is None:
                    aimsg=chunk
                else:
                    aimsg=aimsg+chunk
                ############
                if chunk.content!="":
                    print(chunk.content,end="")
                    #return content
            print("\n")
            message.append(aimsg)
            if aimsg.tool_calls:
                Is_chat_finished=False
                message.append(self.function_call(aimsg))            
            aimsg=None       
            if Is_chat_finished==True:
                print("\n")
                #return XXXX
                break
    def function_call(self,aimsg):
        for tool_calls in aimsg.tool_calls:
            ###############Use tools#############
                #print("test",tool_calls["name"])
                selected_tool = self.tools_dict[tool_calls["name"].lower()]
                tool_output = selected_tool.invoke(tool_calls["args"])
                return ToolMessage(tool_output, tool_call_id=tool_calls["id"])
            #####################################

import asyncio
class LLM_Model_async(LLM_Model):
    def __init__(self, model_type: str="ollama",temperature: float=0.9,tools: list=tools,tools_dict: dict=tools_dict):
        super().__init__()

    async def chat_async(self, qurey:str):
        message=[HumanMessage(qurey)]
        AI_MSGS=""
        chunks=
        async for chunk in self.LLM.astream(message):
            print(chunk)
            if chunk.content!="":
                AI_MSGS+=chunk.content
        print("test",AI_MSGS)
            
        
            
async def test_async():
    print("test_async")



async def main():
    test_model=LLM_Model_async(model_type="ollama",temperature=0.7)
    qurey="你好，请介绍一下你自己"
    task1=asyncio.create_task(test_model.chat_async(qurey))
    task2=asyncio.create_task(test_async())
    await task2
if __name__ == "__main__":
    asyncio.run(main())