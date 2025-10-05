#!/usr/bin/env python3
"""
测试脚本：打印晚报时AI看到的已完成任务列表
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytz
from datetime import datetime, timedelta
from src.get_notion.task_from_notion import fetch_tasks_from_notion
from src.get_env.env_from_notion import get_user_env_vars
from src.utils.time_utils import get_logical_day_dates

def test_night_report_completed_tasks():
    """测试晚报时AI看到的已完成任务"""
    
    print("=" * 60)
    print("测试：晚报时AI看到的已完成任务列表")
    print("=" * 60)
    
    # 获取用户配置
    try:
        user_data = get_user_env_vars()
        if not user_data:
            print("❌ 无法获取用户配置数据，可能需要检查Notion数据库配置")
            print("💡 建议：检查 .env 文件中的 ENV_NOTION_TOKEN 和 ENV_DATABASE_ID")
            return
        
        # 使用第一个用户的配置
        user_id = list(user_data.keys())[0]
        config = user_data[user_id]
        
        print(f"📱 使用用户: {config['USER_NAME']}")
        print(f"⚙️  DAY_END_HOUR: {config['DAY_END_HOUR']}")
        print(f"🌍 TIME_ZONE: {config['TIME_ZONE']}")
        
    except Exception as e:
        print(f"❌ 获取用户配置失败: {e}")
        print("💡 可能的原因:")
        print("   1. Notion数据库中缺少必要字段（如USER_ID）")
        print("   2. .env文件中的token或database_id不正确") 
        print("   3. 网络连接问题（检测到SOCKS代理配置）")
        return
    
    # 获取当前时间
    utc_now = datetime.now(pytz.utc)
    time_zone_offset = int(config["TIME_ZONE"])
    day_end_hour = int(config["DAY_END_HOUR"])
    
    # 转换为用户本地时间
    local_time = utc_now.astimezone(pytz.timezone(f'Etc/GMT{"+" if time_zone_offset < 0 else "-"}{abs(time_zone_offset)}'))
    print(f"🕐 当前本地时间: {local_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 获取逻辑日期
    logical_dates = get_logical_day_dates(local_time, day_end_hour, time_zone_offset)
    logical_today = logical_dates["logical_today"]
    is_early_morning = logical_dates["is_early_morning"]
    
    print(f"📅 逻辑今日: {logical_today}")
    print(f"🌅 是否凌晨: {is_early_morning}")
    
    # 确定要总结的日期（和night_email.py逻辑一致）
    summary_date = logical_today
    print(f"📊 晚报总结日期: {summary_date}")
    
    # 获取任务数据（包含已完成任务）
    print("\n" + "=" * 40)
    print("正在获取任务数据...")
    print("=" * 40)
    
    try:
        tasks = fetch_tasks_from_notion(
            summary_date, 
            config["USER_NOTION_TOKEN"], 
            config["USER_DATABASE_ID"],
            time_zone_offset, 
            include_completed=True,
            day_end_hour=day_end_hour, 
            current_time=local_time
        )
        
        print(f"\n📈 任务统计:")
        print(f"  - 今日到期: {len(tasks['today_due'])} 个")
        print(f"  - 进行中: {len(tasks['in_progress'])} 个") 
        print(f"  - 未来任务: {len(tasks['future'])} 个")
        print(f"  - 已完成: {len(tasks['completed'])} 个")
        
        print(f"\n✅ AI在晚报中看到的已完成任务列表:")
        print("-" * 50)
        
        if not tasks['completed']:
            print("📋 没有在指定时间范围内完成的任务")
        else:
            for i, task in enumerate(tasks['completed'], 1):
                print(f"{i}. {task['Name']}")
                print(f"   ✅ 完成时间: {task['Completed Time']}")
                print(f"   📅 最后编辑: {task['Last Edited']}")
                print(f"   📍 位置: {task['Location']}")
                print(f"   📝 描述: {task['Description']}")
                print(f"   ⚡ 紧急程度: {task['Urgency Level']}")
                print(f"   ⏰ 开始时间: {task['Start Time']}")
                print(f"   ⏱️  结束时间: {task['End Time']}")
                print()
        
        # 显示时间范围逻辑
        print("=" * 50)
        print("🔍 已完成任务筛选逻辑:")
        print("=" * 50)
        
        # 计算时间范围（与task_from_notion.py保持一致）
        tz = pytz.FixedOffset(time_zone_offset * 60)
        today = summary_date
        tomorrow = today + timedelta(days=1)
        
        # 正确的逻辑日边界：从DAY_END_HOUR到DAY_END_HOUR
        today_start = datetime.combine(today, datetime.min.time().replace(hour=day_end_hour)).replace(tzinfo=tz)
        today_end = datetime.combine(tomorrow, datetime.min.time().replace(hour=day_end_hour)).replace(tzinfo=tz)
        
        # 已完成任务的时间范围始终是逻辑日的开始到结束
        completed_end_time = today_end
        time_range_type = "逻辑日范围"
        
        print(f"📅 筛选范围: {today_start.strftime('%Y-%m-%d %H:%M')} 到 {completed_end_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"🎯 模式: 逻辑日范围")
        print(f"💡 判断依据: 任务的'Completed Time'在此范围内（空值会被跳过）")
        
        # 如果有任务，显示第一个任务的详细信息作为示例
        if tasks['completed']:
            print(f"\n📋 示例：第一个已完成任务的时间信息")
            first_task = tasks['completed'][0]
            print(f"   任务名: {first_task['Name']}")
            print(f"   完成时间: {first_task['Completed Time']}")
            print(f"   最后编辑: {first_task['Last Edited']}")
            print(f"   在范围内: ✅")
        
    except Exception as e:
        print(f"❌ 获取任务数据失败: {e}")
        return
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_night_report_completed_tasks()