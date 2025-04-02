from datetime import datetime

def validate_date_format(date_string):
    """验证日期是否符合YYYY-MM-DD格式并返回有效的日期字符串或None"""
    if not date_string:
        return None
        
    try:
        # 尝试解析日期，验证格式和有效性
        parsed_date = datetime.strptime(date_string, "%Y-%m-%d")
        # 再次格式化以确保格式一致
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        try:
            # 如果包含时分秒，解析后只返回日期部分
            parsed_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            # 日期格式无效时返回None
            return None
