
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
			db.cursor().execute("INSERT INTO Besaid_Data(User,Dingo,Condor,Water_Flan) VALUES (?,0,0,0)",(user))
			db.cursor().execute("INSERT INTO kilika_Data(User,Dinonix,Killer_Bee,Yellow_Element,Ragnora) VALUES(?,0,0,0,0)",(user))
			db.cursor().execute("INSERT INTO Mihen_Data(User,Mihen_Fang,Ipiria,Floating_Eye,White_Element,Raldo,Vouivre,Bomb,Dual_horn,Thunder_flan) VALUES(?,0,0,0,0,0,0,0,0,0)",(user))
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
		try:
			username =  session['Current_User']
			return render_template('creatures.html')







		except:
			return render_template('unlogedcreatures.html')


@app.route("/besaid", methods=['POST','GET'])
def Besaid():


		db = get_db()
		username = session['Current_User']
		for item in db.cursor().execute("SELECT *  FROM Besaid_Data WHERE User ='"+ username +"'"):
			dingo = item[1]
			condor = item[2]
			water_flan = item[3]

		if request.method == 'POST':
			db = get_db()
			user = session['Current_User']
			dingo = request.form['Dingo']
			condor = request.form['Condor']
			water_flan = request.form['Water_flan']
			update_Besaid((dingo,condor,water_flan,user))
			return redirect(url_for(".Besaid"))



		return render_template('Besaid.html' , dingo=dingo , condor=condor , water_flan=water_flan)


@app.route("/killika", methods=['POST','GET'])
def Killika():
		db = get_db()
                username = session['Current_User']
               	for item in db.cursor().execute("SELECT *  FROM Kilika_Data WHERE User ='"+ username +"'"):
			Dinonix = item[1]
                       	Killer_bee = item[2]
                       	Yellow_element = item[3]
			Ragnora = item[4]

                if request.method == 'POST':
                        db = get_db()
                        user = session['Current_User']
                        Dinonix = request.form['Dinonix']
                        Killer_bee = request.form['Killer_bee']
                        Yellow_element = request.form['Yellow_element']
			Ragnora = request.form['Ragora']
			update_Killika((Dinonix,Killer_bee,Yellow_element,Ragnora,user))
                        return redirect(url_for(".Killika"))



                return render_template('Killika.html' ,Dinonix=Dinonix,Killer_bee=Killer_bee,Yellow_element=Yellow_element,Ragnora=Ragnora)


@app.route("/mihen", methods=['POST','GET'])
def Mihen():
                db = get_db()
                username = session['Current_User']

                for item in db.cursor().execute("SELECT * FROM Mihen_Data WHERE User ='"+ username +"'"):
       	                Mihen_Fang = item[1]
               	        Ipiria = item[2]
                       	Floating_Eye = item[3]
                       	White_Element = item[4]
			Raldo = item[5]
			Vouivre = item[6]
			Bomb = item [7]
			Dual_Horn = item[8]
			Thunder_flan = item[9]



	       	if request.method == 'POST':
                        db = get_db()
                        user = session['Current_User']
                        Mihen_Fang = request.form['Mihen_Fang']
                        Ipiria = request.form['Ipiria']
			Floating_Eye = request.form['Floating_Eye']
                        White_Element = request.form['White_element']
                        Raldo = request.form['Raldo']
			Vouivre = request.form['Vouivre']
			Bomb = request.form['Bomb']
			Dual_Horn = request.form['Dual_Horn']
			Thunder_flan = request.form['Thunder_Flan']
                        update_Mihen((Mihen_Fang,Ipiria,Floating_Eye,White_Element,Raldo,Vouivre,Bomb,Dual_Horn,Thunder_flan,user))
                        return redirect(url_for(".Mihen"))



                return render_template('Mihen.html',Mihen_Fang=Mihen_Fang,Ipiria=Ipiria,Floating_Eye=Floating_Eye,White_Element=White_Element,Raldo=Raldo,Vouivre=Vouivre,Bomb=Bomb,Dual_Horn=Dual_Horn,Thunder_flan=Thunder_flan)



def update_Besaid(task):

	sql='''UPDATE Besaid_Data
		SET Dingo = ? , 
		 Condor = ?, Water_Flan = ? WHERE User = ?'''

	db = get_db()

	db.execute(sql,task)
	db.commit()

@app.errorhandler(404)
def page_not_found(error):
    return render_template('Error.html'), 404


def update_Killika(task):

        sql='''UPDATE Kilika_Data
                SET Dinonix = ? ,
                 Killer_Bee = ?, Yellow_Element = ? , Ragnora = ? WHERE User = ?'''

        db = get_db()

        db.execute(sql,task)
        db.commit()



def update_Mihen(task):

        sql='''UPDATE Mihen_Data
                SET Mihen_Fang = ? ,
                 Ipiria = ?, Floating_Eye = ? , White_element = ?, Raldo = ? , Vouivre = ? , bomb = ?, dual_Horn = ?, Thunder_flan = ?  WHERE User = ?'''

        db = get_db()

        db.execute(sql,task)
        db.commit()



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=true)
