#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.send_email.email_notifier import send_email

def test_real_email():
    # 模拟真实的邮件内容
    test_body = """
    <h1>测试邮件</h1>
    <h2>今日任务</h2>
    <ul>
        <li>完成邮件服务迁移</li>
        <li>测试邮件发送功能</li>
    </ul>
    <h2>天气信息</h2>
    <p>今天天气晴朗，温度适宜。</p>
    """
    
    EMAIL_RECEIVER = input("请输入收件人邮箱: ")
    EMAIL_TITLE = "LifeSync-AI 测试邮件"
    timeoffset = 8  # 北京时间
    
    print("使用真实代码发送测试邮件...")
    send_email(test_body, EMAIL_RECEIVER, EMAIL_TITLE, timeoffset)

if __name__ == "__main__":
    test_real_email()