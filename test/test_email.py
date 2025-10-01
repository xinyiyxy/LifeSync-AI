#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from alibabacloud_dm20151123.client import Client as DmClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dm20151123 import models as dm_models

# 加载环境变量
load_dotenv()

def test_email():
    # 从环境变量获取配置
    access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    region = os.getenv("ALIYUN_REGION", "cn-hangzhou")
    from_address = os.getenv("EMAIL_FROM_ADDRESS")
    
    print(f"Access Key ID: {access_key_id[:10]}..." if access_key_id else "Access Key ID: Not set")
    print(f"Access Key Secret: {access_key_secret[:10]}..." if access_key_secret else "Access Key Secret: Not set")
    print(f"Region: {region}")
    print(f"From Address: {from_address}")
    
    if not all([access_key_id, access_key_secret, from_address]):
        print("❌ Missing required environment variables!")
        return
    
    try:
        # 创建客户端
        config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret
        )
        config.endpoint = f'dm.{region}.aliyuncs.com'
        config.protocol = 'https'
        config.read_timeout = 30000
        config.connect_timeout = 10000
        client = DmClient(config)
        
        # 测试邮件内容
        to_address = input("请输入收件人邮箱: ")
        
        # 构建邮件发送请求
        request = dm_models.SingleSendMailRequest(
            account_name=from_address,
            address_type=1,
            reply_to_address='false',
            to_address=to_address,
            subject="LifeSync-AI 邮件测试",
            html_body="<h1>测试邮件</h1><p>这是一封来自LifeSync-AI的测试邮件。</p>"
        )
        
        # 发送邮件
        print("正在发送测试邮件...")
        response = client.single_send_mail(request)
        
        if response.status_code == 200:
            print("✅ 邮件发送成功!")
            print(f"Response: {response.body}")
        else:
            print(f"❌ 邮件发送失败. Status: {response.status_code}")
            print(f"Response: {response.body}")
            
    except Exception as e:
        print(f"❌ 发送邮件时出错: {e}")

if __name__ == "__main__":
    test_email()