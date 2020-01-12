#set up server
#import packages
from flask import Flask, request, render_template
from flask_pymongo import PyMongo
from flask import redirect

#initialize
#this function initializes any application
app = Flask(__name__)
app.debug = True

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
    # else:
        # return redirect("/registerStudent")

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
        return redirect("/")

@app.route("/studentList", methods = ['GET', 'POST'])
def list():
    if request.method == 'GET':
        data = mongo.db.user.find({})
        print(data)
        return render_template("studentList.html", data = data)

@app.route("/delete", methods = ['GET', 'POST'])
def delete():
    if request.method == ['GET']:
        return request
#run
if __name__ == "__main__":
    app.run()
