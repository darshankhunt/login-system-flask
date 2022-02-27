
from enum import EnumMeta
from re import M
import sqlite3

from flask.sessions import SessionInterface
'''
# con = sqlite3.connect("web.db")
# print("Database Open Suceessfully.")

# con.execute("create table register (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")
# print("Table Created Sucessfully")

# con.close()
'''
import sqlite3
from flask import *
from flask import session,redirect,url_for,g,request
import os

app = Flask(__name__)
app.secret_key="xyz"
# app.secret_key=os.urandom(24)


@app.route('/')
def sign_up():
    return render_template("register.html")

# @app.route('/login')
# def sign_in():
#     return render_template('login.html')

#For Registration Page:
@app.route('/registration', methods=["POST","GET"])
def insert():
    if request.method=="POST":
        name = request.form["name"]
        email = request.form["email"]
        passw = request.form["pass"]
        rpassw = request.form["re_pass"]
        # term = request.form["agree-term"]
        # # print(type(term))
        # # print(term)
        # demo = "on"


        if name=="" or email=="" or passw=="" or rpassw=="":
            return "<script>alert('All Field are Required.')</script>"
        elif passw != rpassw:
            return "<script>alert('Password and Repeat Password does not match.')</script>"
        # elif term != demo:
        #     return "<script>alert('Please check terms & service!')</script>"
        else:
            try:
                con=sqlite3.connect("web.db")
                cur = con.cursor()
                cur.execute(f"INSERT into register(fname,email,password) values ('{name}','{email}','{passw}')")
                con.commit()
                return render_template("login.html")
            except:
                return "Sorry, Please try after some time!"
    else:
        return "Your Registration is Fail."



#For Login Page:
@app.route('/login',methods=["POST","GET"])
def login():
    # return render_template('login.html')
    if request.method=="POST":
        email = request.form["your_email"]
        passw = request.form["your_pass"]

        con = sqlite3.connect("web.db")
        cur = con.cursor()
        abc = cur.execute("SELECT email,password from register where email='"+email+"' and password='"+passw+"'")
        a1=cur.fetchall()
        count=cur.rowcount
        l1 = []
        for i in a1:
            for j in i:
                l1.append(j)

        # print(l1)
        # print(type(l1))
        # print(l1[0])
        # print(l1[1])
        try:

            if email=="" or passw=="":
                return "<script>alert('Please Fill Username or Password.')</script>"
            elif email==l1[0] and passw==l1[1]:
                session['email'] = request.form['your_email']
                return render_template("web.html")
            # elif count > 1:
            #     return render_template("register.html")
            else:
                return "<script>alert('Enter Correct Username or Password.')</script>"
        except:
                return "<script>alert('Enter Correct Username or Password.')</script>"
    else:
        return render_template("login.html")



'''
@app.route('/login', methods=["POST","GET"])
def login():
    if request.method=='POST':
        session.pop('user',None)

            if request.form['your_pass'] == 'pass':
                session['user'] = request.form['your_email']
                return redirect(url_for('protected'))

    return render_template('login.html')

        email = request.form["your_email"]
        passw = request.form["your_pass"]
        if email=="" or passw=="":
            return "<script>alert('Enter Correct Username or Password.')</script>"
        else:
            try:
                con = sqlite3.connect("web.db")
                cur = con.cursor()
                abc = cur.execute(f"SELECT email,password from register where email='{email}' and password='{passw}'")
                
                print(abc)
                

                for i in abc:
                    print(i[0],i[1])
                    if email == i[0] and passw == i[1]:
                        return render_template('web.html')
                    else:
                        return "<script>alert('Enter Correct Username or Password.')</script>"
            
            except:
                return "invalid Username or Password"
    else:
        return "Your Login Failed."
'''

'''
@app.route(/protected)
def protected():
    if g.user:
        return render_template('web.html',user=session['user'])
    return redirect(url_for('login'))

@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']

@app.route(/dropsession)
def dropsession():
    session.pop('user',None)
    return render_template('login.html')
'''
#for log-out
@app.route('/logout')
def logout():
    return redirect(url_for('login'))

# view Profile data set code.
@app.route('/viewProfile')
def viewProfile():
    if 'email' in session:
        email = session['email']

        con = sqlite3.connect("web.db")
        cur = con.cursor()
        abc = cur.execute("SELECT * from register where email='"+email+"'  ")
        rows = cur.fetchall()
        cur.rowcount
        l1 = []
        for i in rows:
            for j in i:
                l1.append(j)
        print(l1)
        
        dbfname = l1[1]
        print(dbfname)
        return render_template('view.html',data=l1)
    else:
        return '<h2>Please login first</h2>'

@app.route('/web')
def web():
    if 'email' in session:
        email = session['email']
        return render_template('web.html',name=email)
    else:
        return "<h2>You Can't move back.</h2>"

# view Profile update code.
@app.route('/update',methods=["POST","GET"])
def update():
    
    if request.method=="POST":
        fname = request.form['your_fname']
        lname = request.form['your_lname']
        email = session['email']
        # email = request.form['your_email']
        gender = request.form["gen"]
        dob = request.form['dob']
        mono = request.form['mo_no']
        print(fname)
        print(lname)
        print(email)
        print(gender)
        print(dob)
        print(mono)

        con = sqlite3.connect("web.db")
        cur = con.cursor()
        abc = "update register set fname='"+fname+"' , lname = '"+lname+"' , gender = '"+gender+"' , dob = '"+dob+"' , mono = '"+mono+"' where email = '"+email+"' "
        print(abc)
        cur.execute(abc)
        con.commit()
        con.close()

        return "<script>alert('Your data is sucessfullly update.!')</script>"
        # return render_template('view.html')
    else:
        return render_template('view.html')
    # return render_template('view.html')

# session remove code.
@app.route('/sessionremove')
def sessionremove():
    if 'email' in session:
        session.pop('email',None)
        return render_template('login.html')
    else:
        return '<h2>User alredy logged out.</h2>'


if __name__ == "__main__":
    app.run(debug=True)

