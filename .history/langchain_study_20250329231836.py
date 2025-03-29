from model import LLM_Model
from langchain_tools import tools, tools_dict

myllm=LLM_Model(model_type="openai",temperature=0.7,tools=tools,tools_dict=tools_dict)
#qurey="告诉我现在的时间，并计算100+300的结果。"
qurey="推荐一些"
myllm.chat(qurey)


