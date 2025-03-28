import time
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
    
print(get_time("full"))