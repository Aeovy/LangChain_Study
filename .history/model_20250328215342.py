import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage,HumanMessage
from langchain_tools import add,multiply,get_time
from dotenv import load_dotenv
class LLM_Model():
    def __init__(self, model_type: str="ollama",temperature: float=0.9):
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

    def chat(self, qurey:str):
        message=[HumanMessage(qurey)]
        Is_chat_finished=True
        Is_tools_Used=False
        first=True
        aimsg=None
        aimsg_toolcall=None
        while True:
            Is_chat_finished=True
            #print("AI: ",end="")
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
                for tool_calls in aimsg.tool_calls:
                ###############Use tools#############
                    Is_tools_Used=True
                    Is_chat_finished=False
                    #print("test",tool_calls["name"])
                    selected_tool = {"add": add, "multiply": multiply,"get_time":get_time}[tool_calls["name"].lower()]
                    tool_output = selected_tool.invoke(tool_calls["args"])
                    message.append(ToolMessage(tool_output, tool_call_id=tool_calls["id"]))
                #####################################
            
            aimsg=None       
            #print(message)
            if Is_chat_finished:
                break


myllm=LLM_Model(temperature=0.8)
qurey="告诉我现在的时间，并计算100+300的结果。"
myllm.chat(qurey)