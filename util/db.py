import sqlite3

def create():
	'''Creates db and sets up the three tables'''
	DB_FILE="discobandit.db" # db used for this project. delete file if you want to remove all data/login info.
	db = sqlite3.connect(DB_FILE) # Open if file exists, otherwise create
	c = db.cursor()               # Facilitate db operations
	# Creation of three tables as specified in design.pdf. Only created if missing
	c.execute("CREATE TABLE if not exists users(username TEXT, name TEXT, email TEXT, password TEXT)")
	c.execute("CREATE TABLE if not exists user(time TEXT,id TEXT,user TEXT, type TEXT, path TEXT)")
	c.execute("CREATE TABLE if not exists question(name TEXT, id TEXT, author TEXT, upvotes INTEGER, downvotes INTEGER)")



def getPwd(givenUname):
	'''Fetches password for given username'''
	with sqlite3.connect("discobandit.db") as db:
		cur= db.cursor()
		fetchedHash= cur.execute("SELECT password from users WHERE username = ?",(givenUname,)).fetchall()
	return fetchedHash


def newAcct(givenUname,givenName,givenPwd,givenEmail):
	'''Inserts username and password into users table'''
	with sqlite3.connect("discobandit.db") as db:
		cur= db.cursor()
		cur.execute("INSERT INTO users VALUES(?,?,?,?)",(givenUname,givenName,givenEmail,givenPwd)) #inserts hash version of password

def addQuestion(name,id,author,upvotes,downvotes):
	with sqlite3.connect("discobandit.db") as db:
		cur = db.cursor()
		cur.execute("INSERT INTO question VALUES(?,?,?,?,?)",(name,id,author,upvotes,downvotes))

def addUserProblem(time,id,user,status,path):
	with sqlite3.connect("discobandit.db") as db:
		cur = db.cursor()
		cur.execute("INSERT INTO user VALUES(?,?,?,?,?)",(time,id,user,status,path))

def getCreatedProblems(username):
	arr = []
	names = []
	with sqlite3.connect("discobandit.db") as db:
		cur= db.cursor()
		arr= cur.execute("SELECT id from user WHERE user = ? AND type = ?",(username,"created",)).fetchall()
		for id in arr:
			id = id[0]
			name = cur.execute("SELECT name from question WHERE id = ?",(id,)).fetchall()
			names.append(name[0])
		print(names)
	return names

def getInProgressProblems(username):
	arr = []
	names = []
	with sqlite3.connect("discobandit.db") as db:
		cur= db.cursor()
		arr= cur.execute("SELECT id from user WHERE user = ? AND type = ?",(username,"inprog",)).fetchall()
		for id in arr:
			id = id[0]
			name = cur.execute("SELECT name from question WHERE id = ?",(id,)).fetchone()
			names.append(name[0])
	return names

def getDoneProblems(username):
	arr = []
	names = []
	with sqlite3.connect("discobandit.db") as db:
		cur= db.cursor()
		arr= cur.execute("SELECT id from user WHERE user = ? AND type = ?",(username,"done",)).fetchall()
		for id in arr:
			id = id[0]
			name = cur.execute("SELECT name from question WHERE id = ?",(id,)).fetchone()
			names.append(name[0])
	return names

def updateStatus(id, pid):
	with sqlite3.connect("discobandit.db") as db:
		cur= db.cursor()
		name = cur.execute("SELECT name from question WHERE id = ?",(id,)).fetchone()
		name = name[0]
		cur.execute("UPDATE user SET status = ? WHERE user = ? AND id = ?",("inprog",name,pid))


def getID(name):
	with sqlite3.connect("discobandit.db") as db:
		cur= db.cursor()
		id= cur.execute("SELECT id from question WHERE name = ?",(name,)).fetchone()
	return id
