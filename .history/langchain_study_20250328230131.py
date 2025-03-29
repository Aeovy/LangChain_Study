from model import LLM_Model

myllm=LLM_Model(model_type=,temperature=0.8)
#qurey="告诉我现在的时间，并计算100+300的结果。"
qurey="请逐步推理勾股定律"
myllm.chat(qurey)
# while True:
#     qurey=input("请输入问题：")
#     if qurey.lower()=="exit":
#         break
#     elif qurey.lower()=="clear":
#         print("\033[H\033[J",end="")
#         continue
#     elif qurey.lower()=="help":
#         print("输入问题，输入exit退出，输入clear清屏，输入help帮助。")
#         continue
#     else:
#         myllm.chat(qurey)

