from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

# The Form is posted to ‘/setcookie’ URL. 
# The view function sets a Cookie name userID and renders another page.

@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
   if request.method == 'POST':
       user = request.form['nm']
       resp = make_response(render_template('readcookie.html'))
       resp.set_cookie('userID', user)
       return resp

# ‘readcookie.html’ contains a hyperlink to another view function 
# getcookie(), which reads back and displays the cookie value in browser.

@app.route('/getcookie')
def getcookie():
   name = request.cookies.get('userID')
   return '<h1>welcome '+name+'</h1>'


if __name__ == '__main__':
   app.run(debug = True)
