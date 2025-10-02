import pytz
from src.send_email.format_email import format_email
from src.get_notion.task_from_notion import fetch_tasks_from_notion
from src.send_email.email_notifier import send_email
from src.ai_operations.ai_night_advice import email_advice_with_ai
from src.get_wheather import get_weather_forecast
from datetime import datetime
from src.get_env.env_from_notion import get_user_env_vars
from src.utils.time_utils import get_logical_day_dates, get_time_context
from config import SKIP_AI

# Get the current time in UTC, and then convert to the specified UTC offset
utc_now = datetime.now(pytz.utc)
user_data = get_user_env_vars()

for user_id in user_data:
    user_notion_token = user_data[user_id]["USER_NOTION_TOKEN"]
    user_database_id = user_data[user_id]["USER_DATABASE_ID"]
    gpt_version = user_data[user_id]["GPT_VERSION"]
    present_location = user_data[user_id]["PRESENT_LOCATION"]
    user_name = user_data[user_id]["USER_NAME"]
    user_career = user_data[user_id]["USER_CAREER"]
    schedule_prompt = user_data[user_id]["SCHEDULE_PROMPT"]
    time_zone_offset = int(user_data[user_id]["TIME_ZONE"])
    day_end_hour = user_data[user_id]["DAY_END_HOUR"]

    # Convert UTC time to user's local time
    local_time = utc_now.astimezone(pytz.timezone(f'Etc/GMT{"+" if time_zone_offset < 0 else "-"}{abs(time_zone_offset)}'))
    print("local_time: \n" + str(local_time))
    
    # 获取逻辑日期
    logical_dates = get_logical_day_dates(local_time, day_end_hour, time_zone_offset)
    logical_today = logical_dates["logical_today"]
    is_early_morning = logical_dates["is_early_morning"]
    
    print(f"Logical today: {logical_today}")
    print(f"Is early morning: {is_early_morning}")
    
    # 使用逻辑上的"今天"来获取任务
    tasks = fetch_tasks_from_notion(logical_today, user_notion_token, user_database_id, 
                                  time_zone_offset, include_completed=True)

    forecast_data = get_weather_forecast(present_location, time_zone_offset)
    
    # 获取时间上下文
    time_context = get_time_context(local_time, day_end_hour, time_zone_offset)

    data = {
        "weather": forecast_data['tomorrow'],
        # tasks
        "today_tasks": tasks["today_due"],
        "in_progress_tasks": tasks["in_progress"],
        "future_tasks": tasks["future"],
        "completed_tasks": tasks["completed"],
        "time_context": time_context,
        "logical_date": logical_today.strftime('%Y-%m-%d')
    }

    if SKIP_AI:
        print("SKIP_AI=True, 跳过AI生成建议")
        advice = "测试邮件 - AI功能已跳过"
    else:
        advice = email_advice_with_ai(data, gpt_version, present_location, user_career, local_time, schedule_prompt)
    print("Final advice:\n" + advice)

    tittle = "日程晚报"
    time_of_day = "night"
    email_body = f"{format_email(advice, user_name, tittle, time_of_day)}"
    send_email(email_body, user_data[user_id]["EMAIL_RECEIVER"], user_data[user_id]["EMAIL_TITLE"], time_zone_offset)