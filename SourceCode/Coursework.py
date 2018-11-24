
import sqlite3
import bcrypt

from flask import Flask , render_template, g, request, url_for, session, redirect
app = Flask(__name__)
db_location = 'var/Data.db'
app.secret_key = "\zxcvbnm,./asdfghjkl;'#qwertyuiop[]"
user = False

def get_db():
   db = getattr(g, 'db', None)
   if db is None:
   	db = sqlite3.connect(db_location)
   	g.db = db
   return db

@app.teardown_appcontext
def close_db_connection(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
			db.commit()



#home page
@app.route('/home/')
def Home():
	return render_template('home.html')
	db = get_db()
@app.route('/register/', methods=['POST', 'GET'])
def Register():

	db = get_db()
	if request.method == 'POST':
		user = request.form['username']
		pword = request.form['password']
		pword = pword.encode('utf-8')
		hashedpw = bcrypt.hashpw(pword, bcrypt.gensalt())

		if (hashedpw is not None and user is not None):
			db.cursor().execute("INSERT INTO Accounts(uName,pWord) values (?,?)",(user,hashedpw))
			db.commit()
	
	return render_template("register.html")


def check_auth(username, password):
	db = get_db()

	data = db.cursor().execute("SELECT uName,pWord FROM ACCOUNTS")
	data = data.fetchall()
	password = password.encode('utf-8')
	for item in (data):
		if(username == item[0] and item[1].encode('utf-8') == bcrypt.hashpw(password,item[1].encode('utf-8'))):
			return True
	return false

@app.route("/signIn", methods=['Post','GET'])
def signin():
		db = get_db()
		if request.method == 'POST':

			if check_auth(request.form['username'], request.form['password']):
				session['logged in'] = True
				return redirect(url_for('.Home'))

		return render_template('signin.html')


@app.route("/creature", methods=['GET','POST'])
def Creatures():

		if user = True
		







		return render_template('creatures.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=true)
