from datetime import datetime, timedelta
import pytz

def get_logical_day_dates(current_time, day_end_hour, timezone_offset):
    """
    根据"一天结束时间"计算逻辑上的日期
    
    Parameters:
    - current_time: 当前时间 (datetime对象)
    - day_end_hour: 一天结束的小时 (0-23)，例如6表示早上6点
    - timezone_offset: 时区偏移量
    
    Returns:
    - dict: 包含逻辑上的今天、昨天、明天日期
    """
    # 创建时区对象
    tz = pytz.FixedOffset(timezone_offset * 60)
    
    # 确保current_time有时区信息
    if current_time.tzinfo is None:
        current_time = current_time.replace(tzinfo=tz)
    else:
        current_time = current_time.astimezone(tz)
    
    # 获取当前小时
    current_hour = current_time.hour
    current_date = current_time.date()
    
    # 逻辑判断：如果当前时间在day_end_hour之前，认为还是"昨天"
    if current_hour < day_end_hour:
        logical_today = current_date - timedelta(days=1)
        logical_yesterday = current_date - timedelta(days=2)
        logical_tomorrow = current_date
    else:
        logical_today = current_date
        logical_yesterday = current_date - timedelta(days=1)
        logical_tomorrow = current_date + timedelta(days=1)
    
    return {
        "logical_today": logical_today,
        "logical_yesterday": logical_yesterday,
        "logical_tomorrow": logical_tomorrow,
        "is_early_morning": current_hour < day_end_hour
    }

def get_time_context(current_time, day_end_hour, timezone_offset):
    """
    获取时间上下文信息，用于AI生成内容
    
    Returns:
    - str: 时间上下文描述
    """
    dates = get_logical_day_dates(current_time, day_end_hour, timezone_offset)
    
    if dates["is_early_morning"]:
        return f"现在是凌晨{current_time.hour}点，按照您的作息习惯，这还属于{dates['logical_today'].strftime('%Y-%m-%d')}的延续"
    else:
        return f"现在是{current_time.hour}点，新的一天{dates['logical_today'].strftime('%Y-%m-%d')}已经开始"