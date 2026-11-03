"""配置读取：从 config/.env 加载，缺省值保证开箱可跑。"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")

# 邮件报告配置
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.126.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER", "Emily8801@126.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "TBecq33BdLHJEG3H")
MAIL_TO = [x.strip() for x in os.getenv("MAIL_TO", "").split(",") if x.strip()]
MAIL_CC = [x.strip() for x in os.getenv("MAIL_CC", "").split(",") if x.strip()]
MAIL_SUBJECT_PREFIX = os.getenv("MAIL_SUBJECT_PREFIX", "[Login automation testing report]")
