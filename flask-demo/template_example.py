from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<html><body><h1>Hellow World From the h1 Tag</h1></body></html>'

if __name__ == '__main__':
    app.run(debug=True)

