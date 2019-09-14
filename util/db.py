import sqlite3

def create():
	'''Creates db and sets up the three tables'''
	DB_FILE="discobandit.db" # db used for this project. delete file if you want to remove all data/login info.
	db = sqlite3.connect(DB_FILE) # Open if file exists, otherwise create
	c = db.cursor()               # Facilitate db operations
	# Creation of three tables as specified in design.pdf. Only created if missing
	c.execute("CREATE TABLE if not exists users(user TEXT, email TEXT, password TEXT, acctype TEXT, birth TEXT)")
    c.
