from langchain_core.tools import tool
import time 
import sys
import inspect
import ast
import os
from typing import Any
from bilibili_api import search, sync
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
@tool
def search_bilibili(keyword: str) -> dict[Any, Any]:
    """
    Search Bilibili API with the given keyword.
    
    Args:
        keyword: Search term to look for on Bilibili
        
    Returns:
        Dictionary containing the search results from Bilibili
    """
    return sync(search.search(keyword))


def parse_tools_from_source(module):
    source = inspect.getsource(module)
    tree = ast.parse(source)
    tools = []
    tools_dict = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for decorator in node.decorator_list:
                decorator_name = None
                if isinstance(decorator, ast.Name):
                    decorator_name = decorator.id
                elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
                    decorator_name = decorator.func.id
                if decorator_name == "tool":
                    func_name = node.name
                    func = getattr(module, func_name)
                    tools.append(func)
                    tools_dict[func_name] = func
    return tools, tools_dict


# 使用示例
current_module = sys.modules[__name__]
tools, tools_dict = parse_tools_from_source(current_module)




