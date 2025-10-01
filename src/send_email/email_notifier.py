import json
import re
from datetime import datetime
import pytz
from alibabacloud_dm20151123.client import Client as DmClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dm20151123 import models as dm_models
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

        # 创建阿里云邮件推送客户端
        config = open_api_models.Config(
            access_key_id=ALIYUN_ACCESS_KEY_ID,
            access_key_secret=ALIYUN_ACCESS_KEY_SECRET
        )
        config.endpoint = f'dm.{ALIYUN_REGION}.aliyuncs.com'
        client = DmClient(config)

        # 构建邮件发送请求
        single_send_mail_request = dm_models.SingleSendMailRequest(
            account_name=EMAIL_FROM_ADDRESS,
            address_type=1,
            reply_to_address='false',
            to_address=EMAIL_RECEIVER,
            subject=f"{EMAIL_TITLE} {custom_date}",
            html_body=cleaned_body
        )

        # 发送邮件
        response = client.single_send_mail(single_send_mail_request)
        
        if response.status_code == 200:
            print("Email sent successfully!")
        else:
            print(f"Failed to send email. Response: {response.body}")

    except Exception as e:
        print("An error occurred while sending the email:")
        print(e)
