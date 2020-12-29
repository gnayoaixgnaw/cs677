from flask import Flask, request,render_template,redirect
import os
import sqlite3


currentloctation = os.path.dirname(os.path.abspath(__file__))


myapp = Flask(__name__)

@myapp.route("/")
def homepage():
    return render_template('homepage.html')

# @myapp.route("/", methods = ["POST"])
# def checklogin():
#     UN = request.form["Username"]
#     PW = request.form["Passwor"]
#
#     sqlconnection = sqlite3.Connection(currentloctation+"\login.db")
#     cursor = sqlconnection.cursor()
#     query1 = "SELECT Username, Password From Users WHERE Username = {un} AND Password = {pw}".format(un =UN, pw = PW)
#     rows = cursor.execute(query1)
#     rows = rows.fetchall()
#     if len(rows) ==1:
#         return render_template("homepage.html")
#     else:
#         return redirect("register")
# @myapp.route("/register",methods=["GET","POST"])
# def registerpage():
#     if request.method == "POST":
#         dUN = request.form["DUsername"]
#         dPW = request.form['DPassword']
#         Uemail = request.form['Emailuser']
#         sqlconnection = sqlite3.Connection(currentloctation + "\login.db")
#         cursor = sqlconnection.cursor()
#         query1 = "INSERT INTO Users VALUES('{u}','{p}','{e}')".format(u = dUN, p = dPW, e = Uemail)
#         cursor.execute(query1)
#         sqlconnection.commit()
#         return redirect('/')
#     return render_template("homepage.html")

if __name__ == "__main__":
    myapp.run()
