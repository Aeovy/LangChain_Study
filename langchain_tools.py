from langchain_core.tools import tool
import time 
import sys
import inspect
import ast
import os
from typing import Any
import bilibili_api
from bilibili_api import sync
from bilibili_api.search import SearchObjectType
import Functions.Functions as Functions
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
    """获取当前用户的系统时间，支持多种格式输出。
    
    参数:
        format_type: 输出格式选项
            - "default": 标准格式 (YYYY-MM-DD HH:MM:SS)
            - "date": 仅日期 (YYYY-MM-DD)
            - "time": 仅时间 (HH:MM:SS)
            - "full": 完整格式，含星期 (YYYY-MM-DD HH:MM:SS 星期X)
            
    返回:
        str: 按指定格式返回的时间字符串
    """
    now = time.time()
    local_time = time.localtime(now)
    
    if format_type.lower() == "date":
        return time.strftime("%Y-%m-%d", local_time)
    elif format_type.lower() == "time":
        return time.strftime("%H:%M:%S", local_time)
    elif format_type.lower() == "full":
        weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][local_time.tm_wday]
        basic = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        return f"{basic} {weekday}"
    else:  # default
        return time.strftime("%Y-%m-%d %H:%M:%S", local_time)
@tool
def search_bilibili(keyword: str,content_type:str,content_categories:str=None,time_start:str=None,time_end:str=None) :#-> dict[Any, Any]:
    """
    当用户需要在Bilibili(B站，哔哩哔哩)上搜索时，可以使用此工具。
    content_type参数用于指定要搜索的内容的类型，可选值包括：
    ["视频","番剧","影视"  "直播","专栏","话题","用户","直播间用户"],默认为"视频"。
    content_categories参数用于指定内容的分类，可选值包括：
    ["番剧", "电影", "国创", "电视剧", "综艺", "纪录片", "动画",
    "游戏", "鬼畜", "音乐", "舞蹈", "影视", "娱乐", "知识",
    "科技数码", "资讯", "美食", "小剧场", "汽车", "时尚美妆",
    "体育运动"]。如果不指定类型，则搜索所有类型的视频。
    time_start和time_end参数用于指定搜索的时间范围，以日为单位，格式为："YYYY-MM-DD"。
    """
    #get content_categories_id
    content_categories_id=None
    content_categories=["番剧", "电影", "国创", "电视剧", "综艺", "纪录片", "动画", 
                        "游戏", "鬼畜", "音乐", "舞蹈", "影视", "娱乐", "知识", 
                        "科技数码", "资讯", "美食", "小剧场", "汽车", "时尚美妆",
                        "体育运动"]
    if content_categories in content_categories:
        content_categories_id = bilibili_api.video_zone.get_zone_info_by_name(content_categories)[0]["tid"]
    #get content_type
    types_map={
        "视频":SearchObjectType.VIDEO,
        "番剧":SearchObjectType.BANGUMI,
        "影视":SearchObjectType.FT,
        "直播":SearchObjectType.LIVE,
        "专栏":SearchObjectType.ARTICLE,
        "话题":SearchObjectType.TOPIC,
        "用户":SearchObjectType.USER,
        "直播间用户":SearchObjectType.LIVEUSER
    }
    content_type=types_map.get(content_type,SearchObjectType.VIDEO)
    #验证时间合法性
    time_start=Functions.validate_date_format(time_start)
    time_end=Functions.validate_date_format(time_end)
    
    try:
        API_result=sync(bilibili_api.search.search_by_type(keyword=keyword,search_type=content_type,
                                                    video_zone_type=content_categories_id,
                                                    time_start=time_start,
                                                    time_end=time_end,
                                                    ))
        API_result=API_result["result"]
        return_result=[]
        for item in API_result:
            temp={
                "title":item["title"],
                "description":item["description"],
                "author":item["author"],
                "arcurl":item["arcurl"],

            }
            return_result.append(temp)
        return return_result
    except Exception as e:
        e="出错了:"+str(e)
        return e



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



current_module = sys.modules[__name__]
tools, tools_dict = parse_tools_from_source(current_module)




