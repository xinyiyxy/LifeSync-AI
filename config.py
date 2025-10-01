from dotenv import load_dotenv
import os

env_file_loaded = load_dotenv()

ENV_NOTION_TOKEN = os.getenv("ENV_NOTION_TOKEN")
ENV_DATABASE_ID = os.getenv("ENV_DATABASE_ID")

# Email config
ALIYUN_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIYUN_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
ALIYUN_REGION = os.getenv("ALIYUN_REGION", "cn-hangzhou")
EMAIL_FROM_ADDRESS = os.getenv("EMAIL_FROM_ADDRESS")

# OpenAI GPT api
AI_API_KEY = os.getenv("AI_API_KEY")

# Weather API
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")