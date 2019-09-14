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
	c.execute("CREATE TABLE if not exists votes(id TEXT, user TEXT, upordown TEXT)")


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
			names.append(name)
	return names

def getDoneProblems(username):
	arr = []
	names = []
	with sqlite3.connect("discobandit.db") as db:
		cur= db.cursor()
		arr= cur.execute("SELECT id from user WHERE user = ? AND type = ?",(username,"done",)).fetchall()
		for id in arr:
			print("here")
			print(id)
			id = id[0]
			name = cur.execute("SELECT name from question WHERE id = ?",(id,)).fetchone()
			names.append(name)
	return names

def updateStatus(time,pid,id,status,path):
	print("UPDAINTG")
	with sqlite3.connect("discobandit.db") as db:
		cur= db.cursor()
		cur.execute("DELETE FROM user WHERE id = ? AND user = ? AND type = ?",(pid,id,"inprog"))
		cur.execute("INSERT INTO user VALUES(?,?,?,?,?)",(time,pid,id,"done",path))

def checkInProg(id,pid):
	with sqlite3.connect("discobandit.db") as db:
		name = []
		cur= db.cursor()
		name = cur.execute("SELECT path from user WHERE id = ? AND user = ? AND type = ?",(pid,id,"inprog")).fetchall()
		return name
def addProg(time,pid,id,status,path):
	print("UPDAINTG")
	with sqlite3.connect("discobandit.db") as db:
		cur= db.cursor()
		cur.execute("INSERT INTO user VALUES(?,?,?,?,?)",(time,pid,id,"inprog",path))

def storeVote(pid,vote):
	with sqlite3.connect("discobandit.db") as db:
		cur= db.cursor()
		if (vote > 0):
			cur.execute("UPDATE question SET upvotes = upvotes + 1 WHERE id = ?",(pid,))
		else:
			cur.execute("UPDATE question SET downvotes = downvotes + 1 WHERE id = ?",(pid,))
def updateVote(pid,user,vote):
	with sqlite3.connect("discobandit.db") as db:
		cur= db.cursor()
		print("UPDATE")
		if(vote > 0):
			cur.execute("UPDATE votes SET upordown = ? WHERE id = ? AND user = ?",("up",pid,user,))
		else:
			cur.execute("UPDATE votes SET upordown = ? WHERE id = ? AND user = ?",("down",pid,user,))
def didVote(pid,user):
	with sqlite3.connect("discobandit.db") as db:
		cur= db.cursor()
		name = cur.execute("SELECT * from votes WHERE id = ? AND user = ?",(pid,user,)).fetchall()
		print("NAME")
		print(name)
		if (len(name) == 0):
			return False
		else:
			return True
def getPopular():
	with sqlite3.connect("discobandit.db") as db:
		cur= db.cursor()
		arr = cur.execute("SELECT * from question ORDER BY upvotes-downvotes DESC").fetchall()
	return arr
def getID(name):
	with sqlite3.connect("discobandit.db") as db:
		cur= db.cursor()
		id= cur.execute("SELECT id from question WHERE name = ?",(name,)).fetchone()
	return id

def searchKeyword(search):
	with sqlite3.connect("discobandit.db") as db:
		cur= db.cursor()
		arr = cur.execute("SELECT * from question WHERE name LIKE '%"+search+"%' ORDER BY upvotes-downvotes DESC").fetchall()
	return arr;

def getName(id):
	with sqlite3.connect("discobandit.db") as db:
		cur= db.cursor()
		name= cur.execute("SELECT name from question WHERE id = ?",(id,)).fetchone()
	return name[0]
