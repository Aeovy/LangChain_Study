from model import LLM_Model

myllm=LLM_Model(temperature=0.8)

qurey="告诉我现在的时间，并计算100+300的结果。"
myllm.chat(qurey)