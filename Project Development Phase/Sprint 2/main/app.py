from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
from werkzeug.utils import secure_filename
import re
from datetime import timedelta
from flask_session import Session
import ibm_boto3
import os
import os.path
from ibm_botocore.client import Config, ClientError

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
Session(app)
app.secret_key = 'a'
COS_ENDPOINT ="https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
COS_API_KEY_ID ="Zph5PM0Ea1KjdpI2tW6605gi4ms_ewOObsa2AJ23J9Wj"
COS_INSTANCE_CRN ="crn:v1:bluemix:public:cloud-object-storage:global:a/76a3362726624d279ca4e16063b37cd9:07c5e33b-b851-4224-bf7e-8f68f0ced30e::"
cos = ibm_boto3.client(service_name="s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=dcj21936;PWD=SCQV6U0l9lhEOegs",'','')
if conn:
    print("tested")
else:
    exit(0)
#To create table uncomment this
# drop_query="Drop TABLE users if Exists"
# ibm_db.exec_immediate(conn,drop_query)
# create_query="CREATE TABLE users(uname varchar(20) NOT NULL,DOB date NOT NULL,Mobile varchar(20) NOT NULL,email varchar(50) NOT NULL PRIMARY KEY,addr varchar(100) not null,city varchar(20),pincode INTEGER NOT NULL,password varchar(20) NOT NULL,joined TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);"
# ibm_db.exec_immediate(conn,create_query)
# drop_quer="Drop TABLE eligible if Exists"
# ibm_db.exec_immediate(conn,drop_quer)
# create_eligible="CREATE TABLE eligible(elig_email varchar(50) NOT NULL PRIMARY KEY,gender varchar(20) DEFAULT NULL,bg varchar(20) DEFAULT NULL,weight INTEGER DEFAULT NULL,height INTEGER DEFAULT NULL,bmi varchar(20) DEFAULT NULL,chol INTEGER DEFAULT NULL,bp INTEGER DEFAULT NULL,don_date date DEFAULT NULL,certificate varchar(100) DEFAULT NULL,check1 varchar(100) DEFAULT NULL,check2 varchar(100) DEFAULT NULL,check3 varchar(100) DEFAULT NULL);"
# ibm_db.exec_immediate(conn,create_eligible)
# drop_query="Drop TABLE hospital if Exists"
# ibm_db.exec_immediate(conn,drop_query)
# create_query="CREATE TABLE hospital(hospid varchar(20) NOT NULL PRIMARY KEY,name varchar(20),contact INTEGER,location varchar(100),pass varchar(20));"
# ibm_db.exec_immediate(conn,create_query)
# insert_quer="INSERT INTO hospital(hospid,name,contact,location,pass) VALUES ('TN195001123','Varun','123456789','CHENNAI','varun2000')"
# ibm_db.exec_immediate(conn,insert_quer)
@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/check')
def check():
    return render_template('Login.html')

@app.route('/hospitalcheck')
def hoscheck():
    return render_template('hospital_login.html')

@app.route('/addnew')
def addnew():
    return render_template('Register.html')


@app.route('/login',methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' :
        email = request.form['email']
        password = request.form['pass']
        sql = "SELECT * FROM users WHERE email =? AND password =?"
        stmtt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmtt, 1, email)
        ibm_db.bind_param(stmtt, 2, password)
        ibm_db.execute(stmtt)
        account = ibm_db.fetch_assoc(stmtt)
        print(account)
        if account:
            msg=ibm_db.result(stmtt,0)
            msgg=ibm_db.result(stmtt,2)
            session["email"]=email
            session["uname"] = msg
            session["mobile"] = msgg
            return redirect('/dashboard')
        else:
            msg = 'Incorrect username / password !'
            return render_template('Login.html')

@app.route('/hospitallogin',methods =['GET', 'POST'])
def hospitallogin():
    msg = ''
    if request.method == 'POST' :
        ud = request.form['uid']
        password = request.form['pass']
        sql = "SELECT * FROM hospital WHERE hospid =? AND pass =?"
        stmtt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmtt, 1, ud)
        ibm_db.bind_param(stmtt, 2, password)
        ibm_db.execute(stmtt)
        account = ibm_db.fetch_assoc(stmtt)
        print(account)
        if account:
            session["uid"]=ud
            return redirect('/hospitaldashboard')
        else:
            msg = 'Incorrect username / password !'
            return render_template('hospital_login.html')


@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        uname = request.form['name']
        dob = request.form['dob']
        mobile = request.form['contactno']
        email = request.form['email']
        addr = request.form['addr']
        city = request.form['city']
        pin = request.form['pin']
        password = request.form['pass']
        sql = "SELECT * FROM users WHERE email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z]+', uname):
            msg = 'name must contain only characters !'
        else:
            insert_sql = "INSERT INTO  users (uname,DOB,Mobile,email,addr,city,pincode,password) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, uname)
            ibm_db.bind_param(prep_stmt, 2, dob)
            ibm_db.bind_param(prep_stmt, 3, mobile)
            ibm_db.bind_param(prep_stmt, 4, email)
            ibm_db.bind_param(prep_stmt, 5, addr)
            ibm_db.bind_param(prep_stmt, 6, city)
            ibm_db.bind_param(prep_stmt, 7, pin)
            ibm_db.bind_param(prep_stmt, 8, password)
            ibm_db.execute(prep_stmt)
            session["email"]=email
            msg = 'You have successfully registered !'
            return render_template('eligibilty.html')
            # return render_template('Login.html')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('Register.html')


@app.route('/eligibilty', methods =['GET', 'POST'])
def eligibilty():
    msg = ''
    if request.method == 'POST' :
        gender=request.form['gender']
        bg=request.form['bg']
        weight = request.form['weight']
        height = request.form['height']
        ch = request.form['cchk']
        if ch=="Yes":
            chol = request.form['chol']
        bp = request.form['bp']
        bk = request.form['bchk']
        if bk=="Yes":
            don_date = request.form['blood']
            file = request.files['certi']
            file_name=file.filename
            if file_name != '':
                fileam=secure_filename(file.filename)
                file.save(secure_filename(file.filename))
                x=os.path.abspath(fileam)
                with open(x, 'rb') as data:
                    cos.upload_fileobj(data, 'eligibilty-file', fileam)
                os.remove(fileam)
        check1 = request.form.getlist('check1')
        chk1 = ' '.join([str(elem) for elem in check1])
        check2 = request.form.getlist('check2')
        chk2 = ' '.join([str(elem) for elem in check2])
        check3 = request.form.getlist('check3')
        chk3 = ' '.join([str(elem) for elem in check3])
        bmi=(float(weight)/((float(height))*(float(height))))
        sql = "SELECT * FROM users,eligible WHERE users.email=eligible.elig_email AND eligible.elig_email =?"
        stmt = ibm_db.prepare(conn, sql)
        email_elig=session["email"]
        ibm_db.bind_param(stmt, 1, email_elig)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
            return render_template("update_eli.html")
        else:
            if ch=="Yes" and bk=="No":
                insert_sql = "INSERT INTO  eligible(elig_email,gender,bg,weight,height,bmi,chol,bp,check1,check2,check3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                prep_stmt = ibm_db.prepare(conn, insert_sql)
                ibm_db.bind_param(prep_stmt, 1, email_elig)
                ibm_db.bind_param(prep_stmt, 2, gender)
                ibm_db.bind_param(prep_stmt, 3, bg)
                ibm_db.bind_param(prep_stmt, 4, weight)
                ibm_db.bind_param(prep_stmt, 5, height)
                ibm_db.bind_param(prep_stmt, 6, bmi)
                ibm_db.bind_param(prep_stmt, 7, chol)
                ibm_db.bind_param(prep_stmt, 8, bp)
                ibm_db.bind_param(prep_stmt, 9, chk1)
                ibm_db.bind_param(prep_stmt, 10, chk2)
                ibm_db.bind_param(prep_stmt, 11, chk3)
                ibm_db.execute(prep_stmt)
                return redirect('/dashboard')
            elif ch=="Yes" and bk=="Yes":
                if file_name == '':
                    insert_sql = "INSERT INTO  eligible(elig_email,gender,bg,weight,height,bmi,chol,bp,don_date,check1,check2,check3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    prep_stmt = ibm_db.prepare(conn, insert_sql)
                    ibm_db.bind_param(prep_stmt, 1, email_elig)
                    ibm_db.bind_param(prep_stmt, 2, gender)
                    ibm_db.bind_param(prep_stmt, 3, bg)
                    ibm_db.bind_param(prep_stmt, 4, weight)
                    ibm_db.bind_param(prep_stmt, 5, height)
                    ibm_db.bind_param(prep_stmt, 6, bmi)
                    ibm_db.bind_param(prep_stmt, 7, chol)
                    ibm_db.bind_param(prep_stmt, 8, bp)
                    ibm_db.bind_param(prep_stmt, 9, don_date)
                    ibm_db.bind_param(prep_stmt, 10, chk1)
                    ibm_db.bind_param(prep_stmt, 11, chk2)
                    ibm_db.bind_param(prep_stmt, 12, chk3)
                    ibm_db.execute(prep_stmt)
                    return redirect('/dashboard')
                else:
                    fileame=secure_filename(file.filename)
                    insert_sql = "INSERT INTO  eligible(elig_email,gender,bg,weight,height,bmi,chol,bp,don_date,certificate,check1,check2,check3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    prep_stmt = ibm_db.prepare(conn, insert_sql)
                    ibm_db.bind_param(prep_stmt, 1, email_elig)
                    ibm_db.bind_param(prep_stmt, 2, gender)
                    ibm_db.bind_param(prep_stmt, 3, bg)
                    ibm_db.bind_param(prep_stmt, 4, weight)
                    ibm_db.bind_param(prep_stmt, 5, height)
                    ibm_db.bind_param(prep_stmt, 6, bmi)
                    ibm_db.bind_param(prep_stmt, 7, chol)
                    ibm_db.bind_param(prep_stmt, 8, bp)
                    ibm_db.bind_param(prep_stmt, 9, don_date)
                    ibm_db.bind_param(prep_stmt, 10, fileame)
                    ibm_db.bind_param(prep_stmt, 11, chk1)
                    ibm_db.bind_param(prep_stmt, 12, chk2)
                    ibm_db.bind_param(prep_stmt, 13, chk3)
                    ibm_db.execute(prep_stmt)
                    return redirect('/dashboard')
            elif ch=="No" and bk=="No":
                insert_sql = "INSERT INTO  eligible(elig_email,gender,bg,weight,height,bmi,bp,check1,check2,check3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                prep_stmt = ibm_db.prepare(conn, insert_sql)
                ibm_db.bind_param(prep_stmt, 1, email_elig)
                ibm_db.bind_param(prep_stmt, 2, gender)
                ibm_db.bind_param(prep_stmt, 3, bg)
                ibm_db.bind_param(prep_stmt, 4, weight)
                ibm_db.bind_param(prep_stmt, 5, height)
                ibm_db.bind_param(prep_stmt, 6, bmi)
                ibm_db.bind_param(prep_stmt, 7, bp)
                ibm_db.bind_param(prep_stmt, 8, chk1)
                ibm_db.bind_param(prep_stmt, 9, chk2)
                ibm_db.bind_param(prep_stmt, 10, chk3)
                ibm_db.execute(prep_stmt)
                return redirect('/dashboard')
            elif ch=="No" and bk=="Yes":
                if file_name == '':
                    insert_sql = "INSERT INTO  eligible(elig_email,gender,bg,weight,height,bmi,bp,don_date,check1,check2,check3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    prep_stmt = ibm_db.prepare(conn, insert_sql)
                    ibm_db.bind_param(prep_stmt, 1, email_elig)
                    ibm_db.bind_param(prep_stmt, 2, gender)
                    ibm_db.bind_param(prep_stmt, 3, bg)
                    ibm_db.bind_param(prep_stmt, 4, weight)
                    ibm_db.bind_param(prep_stmt, 5, height)
                    ibm_db.bind_param(prep_stmt, 6, bmi)
                    ibm_db.bind_param(prep_stmt, 7, bp)
                    ibm_db.bind_param(prep_stmt, 8, don_date)
                    ibm_db.bind_param(prep_stmt, 9, chk1)
                    ibm_db.bind_param(prep_stmt, 10, chk2)
                    ibm_db.bind_param(prep_stmt, 11, chk3)
                    ibm_db.execute(prep_stmt)
                    return redirect('/dashboard')
                else:
                    fileame=secure_filename(file.filename)
                    insert_sql = "INSERT INTO  eligible(elig_email,gender,bg,weight,height,bmi,bp,don_date,certificate,check1,check2,check3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    prep_stmt = ibm_db.prepare(conn, insert_sql)
                    ibm_db.bind_param(prep_stmt, 1, email_elig)
                    ibm_db.bind_param(prep_stmt, 2, gender)
                    ibm_db.bind_param(prep_stmt, 3, bg)
                    ibm_db.bind_param(prep_stmt, 4, weight)
                    ibm_db.bind_param(prep_stmt, 5, height)
                    ibm_db.bind_param(prep_stmt, 6, bmi)
                    ibm_db.bind_param(prep_stmt, 7, bp)
                    ibm_db.bind_param(prep_stmt, 8, don_date)
                    ibm_db.bind_param(prep_stmt, 9, fileame)
                    ibm_db.bind_param(prep_stmt, 10, chk1)
                    ibm_db.bind_param(prep_stmt, 11, chk2)
                    ibm_db.bind_param(prep_stmt, 12, chk3)
                    ibm_db.execute(prep_stmt)
                    return redirect('/dashboard')
    elif request.method == 'GET':
        msg = 'Please fill out the form !'
    return redirect('/dashboard')



@app.route('/update_elig',methods =['GET', 'POST'])
def update_elig():
    email=session["email"]
    sql = "SELECT * FROM eligible WHERE elig_email =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    if account:
        session["weight"]=ibm_db.result(stmt,3)
        session["height"]=ibm_db.result(stmt,4)
        session["bmi"]=ibm_db.result(stmt,5)
        session["chol"]=ibm_db.result(stmt,6)
        session["bp"]=ibm_db.result(stmt,7)
        session["don_date"]=ibm_db.result(stmt,8)
        session["certificate"]=ibm_db.result(stmt,9)
        session["ck1"]=ibm_db.result(stmt,10)
        session["ck2"]=ibm_db.result(stmt,11)
        session["ck3"]=ibm_db.result(stmt,12)
        bw=request.form['bw']
        if bw=='Yes':
            weight = request.form['weight']
            height = request.form['height']
            if weight!=session["weight"] or height!=session["height"]: 
                bmi=(float(weight)/((float(height))*(float(height))))
                session["weight"]=weight
                session["height"]=height
                session["bmi"]=bmi
        chl=request.form['chl']
        if chl=='Yes':
            chol = request.form['chol']
            if chol!=session["chol"]:
                session["chol"]=chol
        bps=request.form['bps']
        if bps=='Yes':
            bp = request.form['bp']
            if bp!=session["bp"]:
                session["bp"]=bp
        chk_date=request.form['chk_date']
        if chk_date=='Yes':
            don_date = request.form['don_date']
            file = request.files['certi']
            file_name=file.filename
            if don_date!=session["don_date"]:
                if file_name != '':
                    if session["certificate"] is None:
                        fileam=secure_filename(file.filename)
                        session["certificate"]=fileam
                        file.save(secure_filename(file.filename))
                        x=os.path.abspath(fileam)
                        with open(x, 'rb') as data:
                            cos.upload_fileobj(data, 'eligibilty-file', fileam)
                        os.remove(fileam)
                        session["don_date"]=don_date
                    else:
                        cos.delete_object(Bucket='eligibilty-file', Key=session["certificate"])
                        fileam=secure_filename(file.filename)
                        session["certificate"]=fileam
                        file.save(secure_filename(file.filename))
                        x=os.path.abspath(fileam)
                        with open(x, 'rb') as data:
                            cos.upload_fileobj(data, 'eligibilty-file', fileam)
                        os.remove(fileam)
                        session["don_date"]=don_date
                else:
                    if session["certificate"] is not None:
                        cos.delete_object(Bucket='eligibilty-file', Key=session["certificate"])
                        session["certificate"]=None
                        session["don_date"]=don_date
                    else:
                        session["don_date"]=don_date
        ch=request.form['ch']
        if ch=='Yes':
            check1 = request.form.getlist('check1')
            chk1 = ' '.join([str(elem) for elem in check1])
            check2 = request.form.getlist('check2')
            chk2 = ' '.join([str(elem) for elem in check2])
            check3 = request.form.getlist('check3')
            chk3 = ' '.join([str(elem) for elem in check3])
            if chk1!=session["ck1"] or chk2!=session["ck2"] or chk3!=session["ck3"]: 
                session["ck1"]=chk1
                session["ck2"]=chk2
                session["ck3"]=chk3
        print("check")
        if session["don_date"]=='':
            session["don_date"]='2001-10-20'
        sql = "UPDATE eligible SET weight =?, height =?, bmi =?, chol =?, bp =?, don_date =?, certificate =?, check1 =?, check2 =?, check3 =? WHERE elig_email =?"
        stm = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stm, 1, session["weight"])
        ibm_db.bind_param(stm, 2, session["height"])
        ibm_db.bind_param(stm, 3, session["bmi"])
        ibm_db.bind_param(stm, 4, session["chol"])
        ibm_db.bind_param(stm, 5, session["bp"])
        ibm_db.bind_param(stm, 6, session["don_date"])
        ibm_db.bind_param(stm, 7, session["certificate"])
        ibm_db.bind_param(stm, 8, session["ck1"])
        ibm_db.bind_param(stm, 9, session["ck2"])
        ibm_db.bind_param(stm, 10, session["ck3"])
        ibm_db.bind_param(stm, 11, email)
        ibm_db.execute(stm)
        return redirect('/dashboard')
    else:
       return redirect('/eligi')

@app.route('/dashboard')
def dash():
    if not session.get("uname"):
        return redirect("/check")
    msg=session["uname"]
    msgg=session["mobile"]
    return render_template('dashboard.html',msg=msg,msgg=msgg)

@app.route('/hospitaldashboard')
def hospdash():
    if not session.get("uid"):
        return redirect("/hospitalcheck")
    return render_template('hospitaldashboard.html')

@app.route('/elig')
def elig():
    if not session.get("email"):
        return redirect("/check")
    return render_template('update_eli.html')

@app.route('/eligi')
def eligi():
    if not session.get("email"):
        return redirect("/check")
    return render_template('eligibilty.html')

@app.route('/logout')
def logout():
   session["uname"]=None
   session["mobile"]=None
   session["email"]=None
   session["weight"]=None
   session["height"]=None
   session["bmi"]=None
   session["chol"]=None
   session["bp"]=None
   session["don_date"]=None
   session["certificate"]=None
   session["ck1"]=None
   session["ck2"]=None
   session["ck3"]=None
   session["uid"]=None
   return redirect('/')

if __name__ == '__main__':
   app.run(host='0.0.0.0')