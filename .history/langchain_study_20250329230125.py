from model import LLM_Model
from 

myllm=LLM_Model(model_type="openai",temperature=0.7)
#qurey="告诉我现在的时间，并计算100+300的结果。"
qurey="现在几点了？"
myllm.chat(qurey)


