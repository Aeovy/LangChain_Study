from model import LLM_Model

myllm=LLM_Model(model_type="openai",temperature=0.7)
#qurey="告诉我现在的时间，并计算100+300的结果。"
qurey="帮我推荐一下B站上关于初音未来播放量比较高的视频"
myllm.chat(qurey)


