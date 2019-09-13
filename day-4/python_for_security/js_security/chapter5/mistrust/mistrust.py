import os.path
import re
import torndb
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata
import json

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", FormHandler)
        ]
        settings = dict(
            blog_title=u"Mistrust",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            xsrf_cookies=False,
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class FormHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("mistrust.html")

    def post(self):
        print self.get_argument('username')
        print self.get_argument('password')
        data = {
            'success':True
        }
        self.write(data)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()