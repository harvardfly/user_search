from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    def set_default_headers(self):
        """
        解决跨域问题
        :return:
        """
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, DELETE, PUT, PATCH, OPTIONS')
        self.set_header(
            'Access-Control-Allow-Headers',
            'Content-Type, tsessionid, '
            'Access-Control-Allow-Origin, '
            'Access-Control-Allow-Headers, '
            'X-Requested-By, Access-Control-Allow-Methods'
        )

    def options(self, *args, **kwargs):
        pass