import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

from server.utils.time_util import parse_timedelta

load_dotenv()


class DBConfig:
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")
    username = os.getenv("DB_USERNAME", "root")
    password = quote_plus(os.getenv("DB_PASSWORD", "root"))
    database = os.getenv("DB_DATABASE", "ww_test")


class Config:
    db_config = DBConfig()
    # dist相对server根路径的目录,或绝对路径
    ui_root = os.getenv("FB_UI_ROOT", "../admin/dist")
    auth_api = os.getenv("FB_AUTH_API", "/api/system/v1/login")
    auth_salt = os.getenv("FB_AUTH_SALT", "simple-feedback-app-secret")
    auth_expiry = parse_timedelta(os.getenv("FB_AUTH_EXPIRY_TIME", "15m"))


config = Config()
