import os

from dotenv import load_dotenv

load_dotenv()


class DBConfig:
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")
    username = os.getenv("DB_USERNAME", "root")
    password = os.getenv("DB_PASSWORD", "root")
    database = os.getenv("DB_DATABASE", "ww_test")


class Config:
    db_config = DBConfig()


config = Config()
