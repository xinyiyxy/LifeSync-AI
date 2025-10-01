#!/usr/bin/env python3
import os
import requests
import json
import hmac
import hashlib
import base64
from urllib.parse import quote
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_simple_email():
    access_key_id = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    access_key_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    region = os.getenv("ALIYUN_REGION", "cn-hangzhou")
    from_address = os.getenv("EMAIL_FROM_ADDRESS")
    
    print(f"Access Key ID: {access_key_id[:10]}..." if access_key_id else "Access Key ID: Not set")
    print(f"Region: {region}")
    print(f"From Address: {from_address}")
    
    if not all([access_key_id, access_key_secret, from_address]):
        print("❌ Missing required environment variables!")
        return
    
    # 简单测试：使用requests直接调用
    to_address = input("请输入收件人邮箱: ")
    
    # 构建请求参数
    params = {
        'Action': 'SingleSendMail',
        'Version': '2015-11-23',
        'AccessKeyId': access_key_id,
        'SignatureMethod': 'HMAC-SHA1',
        'Timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'SignatureVersion': '1.0',
        'SignatureNonce': str(datetime.now().timestamp()).replace('.', ''),
        'Format': 'JSON',
        'AccountName': from_address,
        'AddressType': '1',
        'ReplyToAddress': 'false',
        'ToAddress': to_address,
        'Subject': 'LifeSync-AI 邮件测试',
        'HtmlBody': '<h1>测试邮件</h1><p>这是一封来自LifeSync-AI的测试邮件。</p>'
    }
    
    try:
        # 构建签名字符串
        sorted_params = sorted(params.items())
        query_string = '&'.join([f'{quote(k, safe="")}={quote(str(v), safe="")}' for k, v in sorted_params])
        string_to_sign = f'POST&%2F&{quote(query_string, safe="")}'
        
        # 计算签名
        signature = base64.b64encode(
            hmac.new(
                (access_key_secret + '&').encode('utf-8'),
                string_to_sign.encode('utf-8'),
                hashlib.sha1
            ).digest()
        ).decode('utf-8')
        
        params['Signature'] = signature
        
        # 发送请求
        url = 'https://dm.aliyuncs.com/'
        print("正在发送测试邮件...")
        
        response = requests.post(url, data=params, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 邮件发送成功!")
            print(f"Response: {result}")
        else:
            print(f"❌ 邮件发送失败. Status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ 发送邮件时出错: {e}")

if __name__ == "__main__":
    test_simple_email()