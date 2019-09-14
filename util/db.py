import sqlite3

def create():
	'''Creates db and sets up the three tables'''
	DB_FILE="discobandit.db" # db used for this project. delete file if you want to remove all data/login info.
	db = sqlite3.connect(DB_FILE) # Open if file exists, otherwise create
	c = db.cursor()               # Facilitate db operations
	# Creation of three tables as specified in design.pdf. Only created if missing
	c.execute("CREATE TABLE if not exists users(username TEXT, name TEXT, email TEXT, password TEXT)")
	c.execute("CREATE TABLE if not exists user(time TEXT,name TEXT, type TEXT, code TEXT)")
	c.execute("CREATE TABLE if not exists question(name TEXT, id TEXT, upvotes INTEGER, downvotes INTEGER)")



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

def addQuestion(name,id,upvotes,downvotes):
	with sqlite3.connect("discobandit.db") as db:
		cur = db.cursor()
		cur.execute("INSERT INTO question VALUES(?,?,?,?)",(name,id,upvotes,downvotes))
