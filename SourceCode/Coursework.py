
import sqlite3
import bcrypt

from flask import Flask , render_template, g, request, url_for, session, redirect
app = Flask(__name__)
db_location = 'var/Data.db'
app.secret_key = "\zxcvbnm,./asdfghjkl;'#qwertyuiop[]"


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
			db.cursor().execute("INSERT INTO Accounts(uName,pWord) VALUES (?,?)",(user,hashedpw))
			db.cursor().execute("INSERT INTO Besaid_Data(User,Dingo,Condor,Water_Flan) VALUES (?,2,3,1)",(user))
			db.commit()
			return redirect(url_for('.signin'))
	return render_template("register.html")


def check_auth(username, password):
	db = get_db()
	data = db.cursor().execute("SELECT uName,pWord FROM Accounts")
	data = data.fetchall()
	password = password.encode('utf-8')
	for item in (data):
			if(username == item[0] and item[1].encode('utf-8') == bcrypt.hashpw(password,item[1].encode('utf-8'))):
				print("ITS ALIVE!!!")
				return True
	return False

@app.route("/signIn", methods=['POST','GET'])
def signin():
		db = get_db()
		if request.method == 'POST':
			username = request.form['username']
			password = request.form['password']

			if check_auth(username,password):
				session['Current_User'] =  username
				print("Working!")
				return redirect(url_for(".Home"))

		return render_template('signin.html')


@app.route("/Creatures", methods=['GET','POST'])
def Creatures():
		db = get_db()


		username =  session['Current_User']
		return render_template('creatures.html')







		#return render_template('unlogedcreatures.html')


@app.route("/besaid", methods=['POST','GET'])
def Besaid():


		db = get_db()
		username = session['Current_User']
		db.cursor().execute("SELECT Dingo FROM Besaid_Data WHERE User ='"+ username +"'")
		dingo = db.cursor().fetchone()
		print(dingo)
		if dingo is None:
			dingo = 0
			print("negative")

		db.cursor().execute("SELECT Condor FROM Besaid_Data WHERE User = ? ",(username))
                condor = db.cursor().fetchone()
                if condor == None:
                        condor = 0

		db.cursor().execute("SELECT Water_Flan FROM Besaid_Data WHERE User =?",(username))
                water_flan = db.cursor().fetchone()
                if water_flan == None:
                        water_flan = 0

		if request.method == 'POST':
			db = get_db()
			user = session['Current_User']
			dingo = request.form.get('dingo')
			condor = request.form.get('condor')
			water_flan = request.form.get('water_flan')
			db.cursor().execute('UPDATE Besaid_Data SET Dingo=?, Condor=?, Water_Flan=? WHERE User=?',(dingo,condor,water_flan,user))
			print(user)
			print("HEEEREEEEE")
			db.commit()
			return render_template('Besaid.html' , dingo=dingo , condor=condor , water_flan=water_flan)




		return render_template('Besaid.html' , dingo=dingo , condor=condor , water_flan=water_flan)




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=true)
