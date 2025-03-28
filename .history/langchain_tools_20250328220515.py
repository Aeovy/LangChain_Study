from langchain_core.tools import tool
import time 
import inspect
import sys
@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b

@tool
def get_time(format_type: str = "default") -> str:
    """获取用户当前本地时间。
    
    参数:
        format_type: 时间格式选项
            - "default": 默认格式 (YYYY-MM-DD HH:MM:SS)
            - "date": 只返回日期 (YYYY-MM-DD)
            - "time": 只返回时间 (HH:MM:SS)
            - "full": 包含星期和毫秒的完整格式
    """
    now = time.time()
    local_time = time.localtime(now)
    
    if format_type.lower() == "date":
        return time.strftime("%Y-%m-%d", local_time)
    elif format_type.lower() == "time":
        return time.strftime("%H:%M:%S", local_time)
    elif format_type.lower() == "full":
        weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][local_time.tm_wday]
        ms = int((now - int(now)) * 1000)
        basic = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        return f"{basic}.{ms:03d} {weekday}"
    else:  # default
        return time.strftime("%Y-%m-%d %H:%M:%S", local_time)





def collect_tools():
    """自动收集当前模块中所有被@tool装饰的函数"""
    # 直接指定已知的工具函数
    tool_functions = [add, multiply, get_time]
    
    # 首先检查一个工具对象的属性
    if tool_functions:
        first_tool = tool_functions[0]
        print(f"Tool type: {type(first_tool)}")
        print(f"Tool dir: {dir(first_tool)}")
    
    # 创建工具列表和工具字典
    tools_list = tool_functions
    # 使用name属性而不是__name__
    tools_mapping = {func.name: func for func in tool_functions}
    
    return tools_list, tools_mapping


tools, tools_dict = collect_tools()

print(tools)
print(tools_dict)
#tools=[add,multiply,get_time]
#tools_dict={"add": add, "multiply": multiply,"get_time":get_time}


