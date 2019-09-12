from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_index():
    return 'Hello Everyone!!!'

@app.route('/hello')
def hello_world():
    return 'Hello World'

@app.route('/hello/<name>')
def hello_name(name):
    return 'Hello %s!' % name
@app.route('/blog/<int:postID>')
def show_blog(postID):
    return 'Blog Number %d' % postID
@app.route('/rev/<float:revNo>')
def revision(revNo):
    return 'Revision number %f' % revNo

@app.route('/flask')
def hello_flask():
    return 'Hello FLask'

@app.route('/python/')
def hello_python():
    return 'Hello From Canonical Python Route'

def revision(revNo):
    return 'Revision number %f' % revNo

if __name__ == '__main__':
    app.run(debug=True)
