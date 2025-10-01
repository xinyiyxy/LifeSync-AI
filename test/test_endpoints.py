#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from alibabacloud_dm20151123.client import Client as DmClient
from alibabacloud_tea_openapi import models as open_api_models

load_dotenv()

def test_endpoints():
    access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    
    if not all([access_key_id, access_key_secret]):
        print("❌ Missing credentials!")
        return
    
    # 尝试不同的endpoint
    endpoints = [
        'dm.cn-hangzhou.aliyuncs.com',
        'dm.aliyuncs.com',
        'dm.ap-southeast-1.aliyuncs.com',
        'dm.cn-beijing.aliyuncs.com'
    ]
    
    for endpoint in endpoints:
        try:
            print(f"\n🔍 Testing endpoint: {endpoint}")
            
            config = open_api_models.Config(
                access_key_id=access_key_id,
                access_key_secret=access_key_secret
            )
            config.endpoint = endpoint
            config.read_timeout = 10000
            config.connect_timeout = 5000
            
            client = DmClient(config)
            
            # 只测试连接，不发送邮件
            print(f"✅ 连接成功: {endpoint}")
            
        except Exception as e:
            print(f"❌ 连接失败: {e}")
    
    print("\n推荐使用: dm.aliyuncs.com (全球通用endpoint)")

if __name__ == "__main__":
    test_endpoints()