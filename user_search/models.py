# coding:utf-8

import time
from user_search.settings import database
from peewee import *


def get_current_timestamp():
    """
    获取当前时间戳
    :return:
    """
    return int(time.time() * 1000)


class BaseModel(Model):
    create_time = BigIntegerField(
        default=get_current_timestamp,
        verbose_name="创建时间"
    )
    update_time = BigIntegerField(
        default=get_current_timestamp,
        verbose_name="修改时间"
    )

    class Meta:
        database = database
