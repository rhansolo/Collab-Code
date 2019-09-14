import os
import sqlite3
import datetime,os
import util.db as db
from flask import Flask, render_template, request, session, url_for, redirect, flash
from passlib.hash import pbkdf2_sha256


db.create()
app = Flask(__name__)
app.secret_key=os.urandom(32)# 32 bits of random data as a string

@app.route("/")
def homepage():
	'''Displays appropriate homepage based on whether user is logged in.'''
	if session.get("uname"):
		username = session["uname"]
		return render_template("loggedIn.html", user = username)
	return render_template("login.html",Title = 'Login')

@app.route("/newUser", methods=['POST','GET'])
def createAcct():
	'''Used to access Create New User functionality'''
	return render_template("newUser.html")

@app.route("/addUser", methods=['POST'])
def addAcct():
    givenUname=request.form["username"]
    givenPwd=request.form["password"]
    givenEmail=request.form["email"]
    givenName = request.form["name"]
    confirmPwd = request.form["confirm_password"]
    hash = pbkdf2_sha256.hash(givenPwd)
    if (len(givenUname)==0 or len(givenPwd)==0):
        flash('Username/Password cannot be 0 characters long')
        return redirect(url_for("createAcct"))
    if (confirmPwd != givenPwd):
        flash("Paswords don't match. Please try again!")
        return redirect(url_for("createAcct"))
    fetchedPass=db.getPwd(givenUname)
    if (len(fetchedPass) == 0):
        db.newAcct(givenUname,givenName,hash,givenEmail)
    else:
        flash("USER NAME ALREADY EXISTS PLS TRY AGAIN")
        return redirect(url_for("createAcct"))
    return redirect(url_for("homepage"))

@app.route("/authenticate", methods=['POST'])
def callback():
	'''Authentication route used to log user in'''
	givenUname=request.form["username"]
	givenPwd=request.form["password"]
	fetchedHash=db.getPwd(givenUname)
	if fetchedHash:
		if pbkdf2_sha256.verify(givenPwd, fetchedHash[0][0]):
			#fix since fetchall returns a list of tuples
			session["uname"]= givenUname #stores givern username in session
			return redirect(url_for("homepage"))
		else:
			flash('Password is wrong!')
			return redirect(url_for("homepage"))
	else:
		flash('Username is wrong!')
		return redirect(url_for("homepage"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
