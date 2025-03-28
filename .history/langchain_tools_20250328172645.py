from langchain_core.tools import tool
import time 
@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b
@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b
@tool
def getlocaltime(a:bool) -> str :
    """Get User's local time,input True if you need to use this function"""
    local_time=time.localtime(time.time())
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    return formatted_time

tools=[add,multiply,getlocaltime]


