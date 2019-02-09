import sys

sys.path.append("/vagrant/user_search/")

from apps.users.models import User
from user_search.settings import database


def init():
    # 生成表
    database.create_tables([User], safe=True)


if __name__ == "__main__":
    init()
