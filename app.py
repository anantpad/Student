#set up server
#import packages
from flask import Flask, request, render_template
from flask_pymongo import PyMongo
from flask import redirect, session, flash
from datetime import datetime, date

#initialize
#this function initializes any application
app = Flask(__name__)
app.debug = True

app.secret_key = "sri"

#config
app.config["MONGO_URI"] = "mongodb://sridhar:asdf@cluster0-shard-00-00-aou9c.mongodb.net:27017,cluster0-shard-00-01-aou9c.mongodb.net:27017,cluster0-shard-00-02-aou9c.mongodb.net:27017/studentdb?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
# app.config["MONGO_URI"] = "mongodb://sridhar:asdf@cluster0-aou9c.mongodb.net/test?retryWrites=true&w=majority"

mongo = PyMongo(app)
print(mongo.db)

#route
@app.route("/", methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:

        studentid = request.form["studentid"]
        session["loggedin"] = studentid
        flash("Checked in successfully")
        print(session)
        checkintime = datetime.now()
        checkinday = checkintime.strftime("%a")
        checkindate = checkintime.strftime("%d")
        checkinmonth = checkintime.strftime("%b")
        checkinyear = checkintime.strftime("%Y")

        mongo.db.attendance.update_one(
            {"studentid":studentid},{"$set":{"checkindate":checkindate,"checkintime":checkintime,"checkinday":checkinday,"checkinmonth":checkinmonth,"checkinyear":checkinyear}},upsert=True
        )
        return redirect("/attendance")

@app.route("/registerStudent", methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("User.html")
    else:
        studentid = request.form["studentid"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        mi = request.form["mi"]
        gender = request.form["gender"]
        birthdate = request.form["birthdate"]
        mongo.db.user.insert_one(
            {"studentid": studentid, "firstname": firstname, "lastname": lastname, "mi": mi, "gender": gender,
             "birthdate": birthdate})
        flash("Student successfully registered")
        return redirect("/")

@app.route("/studentList", methods = ['GET', 'POST'])
def list():
    if request.method == 'GET':
        data = mongo.db.user.find({})
        print(data)
        return render_template("studentList.html", data = data)

@app.route("/editStudent", methods = ['GET', 'POST'])
def editStudent():
    if request.method == 'GET':
        studentid = request.args['studentid']
        record = mongo.db.user.find_one({"studentid":studentid})
        firstname = record["firstname"]
        # contents of this variable is the value of the input field
        # GET, request.args gives argument fro URL
        print(studentid)
        return render_template('editUser.html',studentid=studentid, firstname=firstname)
    # studentid=studentid :: name of variable on html template : variable studentid in the above function
    else:
        studentid = request.form["studentid"]
        # REQUEST.FORM is from input field, name attribute
        # contents of this variable is the value of the input field
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        mi = request.form["mi"]
        gender = request.form["gender"]
        birthdate = request.form["birthdate"]
        mongo.db.user.update_one(
            {"studentid": studentid},{"$set":{"firstname": firstname, "lastname": lastname, "mi": mi, "gender": gender,
            "birthdate": birthdate}})
        return redirect('/studentList')

@app.route("/attendance", methods = ['GET', 'POST'])
def attndlist():
    if request.method == 'GET':
        if "loggedin" not in session:
            return redirect("/")
        # elif session["loggedin"] != True:
        #     return redirect("/")

        attenddata = mongo.db.attendance.find({})
        return render_template("attendance.html", attenddata = attenddata)

@app.route("/delete", methods = ['GET', 'POST'])
def delete():
    if request.method == 'GET':
        studentid = request.args['studentid']
        print(studentid)
        mongo.db.user.delete_one({'studentid':studentid})
        return redirect("/studentList")

@app.route("/logout", methods = ['GET'])
def logout():
    session.pop("loggedin",None)
    print(session)
    return redirect("/")


#run
if __name__ == "__main__":
    app.run()
