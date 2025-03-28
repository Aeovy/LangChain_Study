from langchain_core.tools import tool
import time 
import sys
import inspect
import ast
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


def parse_tools_from_module(module):
    """解析模块源码，提取被 @tool 装饰的工具实例"""
    source = inspect.getsource(module)
    tree = ast.parse(source)
    tool_functions = []
    
    # 第一步：找到所有被 @tool 装饰的函数名
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for decorator in node.decorator_list:
                decorator_name = None
                # 处理普通装饰器（如 @tool）
                if isinstance(decorator, ast.Name):
                    decorator_name = decorator.id
                # 处理带参数的装饰器（如 @tool(name="xxx")）
                elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
                    decorator_name = decorator.func.id
                if decorator_name == "tool":
                    tool_functions.append(node.name)
    
    # 第二步：从模块中获取对应的工具实例
    tools = []
    tools_dict = {}
    for func_name in tool_functions:
        func = getattr(module, func_name)  # 这里获取的是 StructuredTool 实例
        tools.append(func)
        tools_dict[func.name] = func  # 使用工具实例的 name 属性
    
    return tools, tools_dict

# 使用示例
current_module = sys.modules[__name__]
tools, tools_dict = parse_tools_from_module(current_module)

# print("Tools:", tools)
#print("Tools Dictionary:", tools_dict)

print(tools[0].func)
print(type(tools[0].func))


# tools=[add,multiply,get_time]
# tools_dict={"add": add, "multiply": multiply,"get_time":get_time}


