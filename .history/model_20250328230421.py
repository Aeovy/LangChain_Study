import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage,HumanMessage
from langchain_tools import add,multiply,get_time,tools,tools_dict
from dotenv import load_dotenv
class LLM_Model():
    def __init__(self, model_type: str="ollama",temperature: float=0.9,tools: list=tools,tools_dict: dict=tools_dict):
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
        if tools:
            self.LLM = self.LLM.bind_tools(tools)
        if tools_dict:
            self.tools_dict = tools_dict
        self.history_message =None
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
                    #or return content
                    #pass
            message.append(aimsg)
            if aimsg.tool_calls:
                Is_chat_finished=False
                message.append(self.function_call(aimsg))            
            aimsg=None       
            if Is_chat_finished:
                print("\n")
                break
    def function_call(self,aimsg):
        for tool_calls in aimsg.tool_calls:
            ###############Use tools#############
                #print("test",tool_calls["name"])
                selected_tool = self.tools_dict[tool_calls["name"].lower()]
                tool_output = selected_tool.invoke(tool_calls["args"])
                return ToolMessage(tool_output, tool_call_id=tool_calls["id"])
            #####################################