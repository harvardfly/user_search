import os

import peewee_async
from .settings_local import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# setting配置放在settings_local下，防止暴露数据库信息
settings = settings
database = peewee_async.MySQLDatabase(
    **settings["db"]
)
