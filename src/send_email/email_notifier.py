import json
import re
import requests
import hmac
import hashlib
import base64
from urllib.parse import quote
from datetime import datetime
import pytz
from config import ALIYUN_ACCESS_KEY_ID, ALIYUN_ACCESS_KEY_SECRET, ALIYUN_REGION, EMAIL_FROM_ADDRESS

def send_email(body, EMAIL_RECEIVER, EMAIL_TITLE, timeoffset):
    print("Sending email...")
    try:
        # 使用正则表达式清理body中的Markdown代码块标记
        cleaned_body = re.sub(r'```(?:html)?', '', body)  # 删除```和```html

        # 获取当前 UTC 时间
        utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
        
        # 根据时区偏移量创建时区并转换时间
        timezone_str = f'Etc/GMT{"+" if timeoffset < 0 else "-"}{abs(timeoffset)}'
        local_timezone = pytz.timezone(timezone_str)
        local_now = utc_now.astimezone(local_timezone)
        custom_date = local_now.strftime('%Y-%m-%d')

        # 构建请求参数
        params = {
            'Action': 'SingleSendMail',
            'Version': '2015-11-23',
            'AccessKeyId': ALIYUN_ACCESS_KEY_ID,
            'SignatureMethod': 'HMAC-SHA1',
            'Timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'SignatureVersion': '1.0',
            'SignatureNonce': str(datetime.now().timestamp()).replace('.', ''),
            'Format': 'JSON',
            'AccountName': EMAIL_FROM_ADDRESS,
            'AddressType': '1',
            'ReplyToAddress': 'false',
            'ToAddress': EMAIL_RECEIVER,
            'Subject': f"{EMAIL_TITLE} {custom_date}",
            'HtmlBody': cleaned_body
        }
        
        # 构建签名字符串
        sorted_params = sorted(params.items())
        query_string = '&'.join([f'{quote(k, safe="")}={quote(str(v), safe="")}' for k, v in sorted_params])
        string_to_sign = f'POST&%2F&{quote(query_string, safe="")}'
        
        # 计算签名
        signature = base64.b64encode(
            hmac.new(
                (ALIYUN_ACCESS_KEY_SECRET + '&').encode('utf-8'),
                string_to_sign.encode('utf-8'),
                hashlib.sha1
            ).digest()
        ).decode('utf-8')
        
        params['Signature'] = signature
        
        # 发送请求
        url = 'https://dm.aliyuncs.com/'
        response = requests.post(url, data=params, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'EnvId' in result:
                print("Email sent successfully!")
            else:
                print(f"Failed to send email. Response: {result}")
        else:
            print(f"Failed to send email. Status code: {response.status_code}, Response: {response.text}")

    except Exception as e:
        print("An error occurred while sending the email:")
        print(e)
