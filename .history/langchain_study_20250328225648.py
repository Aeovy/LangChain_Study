from model import LLM_Model

myllm=LLM_Model(temperature=0.8)
while True:
    qurey=input("请输入问题：")
    if qurey.lower()=="exit":
        break
    elif qurey.lower()=="clear":
        print("\033[H\033[J",end="")
        continue
    elif qurey.lower()=="help":
        print("输入问题，输入exit退出，输入clear清屏，输入help帮助。")
        continue
