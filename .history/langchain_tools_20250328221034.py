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



# 自动收集所有被@tool装饰的函数
def get_all_tools():
    current_module = sys.modules[__name__]
    tool_functions = []
    tool_dict = {}
    
    # 打印当前模块名称，确认我们在正确的模块中
    print(f"当前模块: {__name__}")
    
    for name, obj in inspect.getmembers(current_module):
        # 检查是否为函数
        if inspect.isfunction(obj):
            print(f"发现函数: {name}, 属性: {dir(obj)[:5]}...")
            # 尝试检查不同可能的属性名称
            if hasattr(obj, 'runnable'):
                tool_functions.append(obj)
                # 获取工具名称，可能需要根据实际属性调整
                tool_name = obj.runnable.name if hasattr(obj.runnable, 'name') else name
                tool_dict[tool_name] = obj
                print(f"  - 已添加工具: {tool_name}")
            # 备选属性检查
            elif hasattr(obj, '_type') and obj._type == 'tool':
                tool_functions.append(obj)
                tool_dict[name] = obj
                print(f"  - 已添加工具(备选方式): {name}")
    
    return tool_functions, tool_dict


# 自动生成tools和tools_dict
tools, tools_dict = get_all_tools()
print(tools)
print(tools_dict)

# tools=[add,multiply,get_time]
# tools_dict={"add": add, "multiply": multiply,"get_time":get_time}


