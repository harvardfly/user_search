# coding:utf-8
import tornado
from tornado import web
from peewee_async import Manager
from user_search.urls import urlpattern
from user_search.settings import (
    settings, database
)

if __name__ == "__main__":
    import wtforms_json

    # 把json集成到 wtforms里面
    wtforms_json.init()

    app = web.Application(urlpattern, debug=True, **settings)
    app.listen(8888)

    objects = Manager(database)
    database.set_allow_sync(False)
    app.objects = objects

    tornado.ioloop.IOLoop.current().start()
