from tornado.web import url
from apps.users.handler import (
    RegisterHandler,
    EsUserSearchHandler
)

urlpattern = (
    url("/register/", RegisterHandler),
    url("/search", EsUserSearchHandler),
)
