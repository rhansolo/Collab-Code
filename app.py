import os
import pickle
import sqlite3
import datetime,os
import os,binascii
import util.db as db
from runner import runner
from flask import Flask, render_template, request, session, url_for, redirect, flash, jsonify
from passlib.hash import pbkdf2_sha256


db.create()
app = Flask(__name__, static_url_path='', static_folder='static')
app.secret_key=os.urandom(32)# 32 bits of random data as a string
is_progress_flag = False
is_done_flag = False

@app.route("/")
def homepage():
	'''Displays appropriate homepage based on whether user is logged in.'''
	if session.get("uname"):
		username = session["uname"]
		return render_template("loggedIn.html", user = username, arr1 = db.getCreatedProblems(username),arr2 =db.getInProgressProblems(username),arr3=db.getDoneProblems(username),arr4 = db.getPopular())
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

@app.route("/newproblem", methods=['GET'])
def createNewProblem():
	return render_template("createProblem.html")

@app.route("/storeproblem", methods=['POST'])
def store():
    if not session.get("uname"):
	       return redirect(url_for("homepage"))
    problemName = request.form["problemName"]
    problem = request.form["problem"]
    test_cases = [(request.form['t'+str(i)].split(), request.form['s'+str(i)].split()) for i in range(1, 11) if request.form['t'+str(i)] != '']
    solution = request.form["solution"]

    to_save = (problem, test_cases, solution)
    binascii.b2a_hex(os.urandom(15))
    tmp = gen_rand()
    tmp = tmp[2:-1]
    path = './problems/'+tmp+'.p'
    while (os.path.exists(path)):
        tmp = gen_rand()
        path = './problems/'+tmp+'.p'
    file = open(path, 'wb+')
    pickle.dump(to_save, file)
    db.addQuestion(problemName,tmp,session["uname"],0,0)
    db.addUserProblem(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),tmp,session["uname"],"created",path)
    flash('Problem created!')
    return redirect(url_for("homepage"))

@app.route('/logout',methods=['POST','GET'])
def logout():
	'''Route logs the user out if they are logged in'''
	if not session.get("uname"):
		return redirect(url_for("homepage"))
	session.pop('uname') #ends session
	return redirect(url_for('homepage')) #goes to home, where you can login

@app.route('/edit', methods = ['POST','GET'])
def edit():
    if not session.get("uname"):
        return redirect(url_for("homepage"))
    questionTitle=request.args.get("title")
    print(questionTitle)
    return redirect(url_for('display',name = questionTitle))

@app.route('/search',methods = ['POST','GET'])
def search():
	if not session.get("uname"):
		return redirect(url_for("homepage"))
	search = request.form['query']
	arr = db.searchKeyword(search)
	print(arr)
	return render_template("results.html",arr = arr, keyword = search)
@app.route('/vote',methods = ['POST'])
def vote():
	try:
		pid = request.form['Submit1']
		name = db.getName(pid);
		vote = 1
		db.storeVote(pid,vote);
		db.updateVote(pid,session["uname"],vote);
		return redirect(url_for('display', name = name))
	except:
		pid = request.form['Submit2']
		name = db.getName(pid);
		vote = -1
		db.storeVote(pid,vote);
		db.updateVote(pid,session["uname"],vote);
		return redirect(url_for('display', name = name))

@app.route('/problem/<name>',methods=['POST','GET'])
def display(name):
	id = db.getID(name)
	id = id[0]
	file_name = './problems/' + id + '.p'
	problem = pickle.load(open(file_name, 'rb'))[0]
	print(id)
	bool = db.didVote(id,session["uname"])
	print(bool)
	return render_template("index.html", problemstate= problem,pid = id,user =session["uname"],problemname = name,voted = bool)

@app.route('/get_code/<id>/<pid>/<lang>')
def get_code(id,pid,lang):
    dict = {"Solution.java":"public class Solution {\n    public static void main(String[] args) {\n        \n    }\n}",
        "Solution.cpp" : "#include <bits/stdc++.h>\n\nusing namespace std;\n\nint main(int argc, char** argv) {\n    return 0;\n}",
        "Solution.py": "if __name__ == '__main__':\n    "}
    path = "./working/"+id + "_" + pid
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, lang)
    if (os.path.exists(path)):
        file = open(path,"r")
        return file.read()
    else:
        file = open(path,"w+")
        file.write(dict[lang])
        file.close()
        return dict[lang]

@app.route('/write_code/<id>/<pid>/<lang>',methods = ['POST','GET'])
def write_code(id,pid,lang):
	if request.method == 'POST':
		path = "./working/"+id + "_" + pid
		path = os.path.join(path, lang)
		file = open(path,"w+")
		file.write(request.json['code'])
		file.close()
		if (len(db.checkInProg(id,pid)) == 0):
			print("IN PROGRESS")
			db.addProg(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),pid,id,"inprog",path)
		return "fuck you"

@app.route('/submit/<id>/<pid>/<lang>')
def submit(id,pid,lang):
	questionpath = "problems/" + pid + ".p"
	questionpath = os.path.abspath(questionpath)
	solutionpath = "working/"+id + "_" + pid
	solutionpath = os.path.join(solutionpath, lang)
	solutionpath = os.path.abspath(solutionpath)
	#tmp = runner.run_java(solutionpath,questionpath)
	tmp = ""
	if (lang == "Solution.java"):
		tmp = runner.run_java(solutionpath, questionpath)
	elif (lang == "Solution.py"):
		tmp = runner.run_python(solutionpath,questionpath)
	elif (lang == "Solution.cpp"):
		tmp = runner.run_cpp(solutionpath,questionpath)
	if (not tmp == "" and (len(set(tmp)) == 1 and tmp[0] == 'c')):
		print("IS DONE")
		db.updateStatus(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),pid,id,"done","./working/"+id + "_" + pid)

	print(tmp)
	return jsonify(tmp)


def gen_rand():
    return str(binascii.b2a_hex(os.urandom(15)))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
