import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from pymong import MongoClient
from bson.objectid import ObjectId
from tornado_cors import CorsMixin
from tornado.options import define, options
import json
import os
define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/api/todos", Todos),
            (r"/todo", TodoApp),
            (r"/todo_external", TodoAppExternal)

        ]
        conn = MongoClient()
        self.db = conn.todos
        settings = dict(
            xsrf_cookies=False, # this will need to be changed to True
            debug=True,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static")
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class TodoApp(tornado.web.RequestHandler):
    def get(self):
        self.render("todos.html")

class TodoAppExternal(tornado.web.RequestHandler):
    def get(self):
        self.render("external.html")


class Todos(tornado.web.RequestHandler):
    # see how can i change this to GET and can change data ?
    # this can be used to reflect the XSS attack here:
    # http://stackoverflow.com/questions/2526522/csrf-cross-site-request-forgery-attack-example-and-prevention-in-php
    def get(self):


        Todos = self.application.db.todos
        todo_id = self.get_argument("id", None)

        if todo_id:
            todo = Todos.find_one({"_id": ObjectId(todo_id)})
            todo["_id"] = str(todo['_id'])
            self.write(todo)
        else:
            todos = Todos.find()
            result = []
            data = {}
            for todo in todos:
                todo["_id"] = str(todo['_id'])
                result.append(todo)
            data['todos'] = result
            self.write(data)


    def post(self):


        Todos = self.application.db.todos
        todo_id = self.get_argument("id", None)

        if todo_id:
            # perform a delete for example purposes
            todo = {}
            print "deleting"
            Todos.remove({"_id": ObjectId(todo_id)})
            # cos _id is not JSON serializable.
            todo["_id"] = todo_id
            self.write(todo)
        else:
            todo = {
                'text': self.get_argument('text'),
                'details': self.get_argument('details')
            }
            a = Todos.insert(todo)
            todo['_id'] = str(a)
            self.write(todo)



def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
