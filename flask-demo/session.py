from flask import Flask, session, redirect, url_for, escape, request
from flask_session import Session

app = Flask(__name__)
SESSION_TYPE = 'filesystem' 
app.config.from_object(__name__)
Session(app)
app.secret_key = 'any random string'


@app.route('/')
def index():
    session['username'] = 'admin'
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + \
         "<b><a href = '/logout'>click here to log out</a></b>"
    return "You are not logged in <br><a href = '/login'></b>" + \
      "click here to log in</b></a>"

@app.route('/login', methods = ['GET', 'POST'])
def login():
		# a form is posted back to login
   if request.method == 'POST':
      session['username'] = request.form['username']
			# if the username is found, redirect to index
      return redirect(url_for('index'))
   return '''

   <form action = "" method = "post">
      <p><input type = text name = username/></p>
      <p<<input type = submit value = Login/></p>
   </form>

   '''


@app.route('/logout')
def logout():
# remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
   app.run(debug = True)
