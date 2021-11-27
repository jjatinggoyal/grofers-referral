DB_HOST = "dpg-c6ggsq76d9kjo81csesg"
DB_NAME = "grofers"
DB_USER = "jatin"
DB_PASS = "8NsKIkmrpntNEns2lRXCWRzyKjozE7Qo"
DB_PORT = "5432"

from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras
import hashlib

app = Flask(__name__)


@app.route("/admin")
def hello():
    # conn = psycopg2.connect(dbname="grofers", user="postgres", password="jatin", host="localhost", port="5432")
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("select * from users")
    formdata = cur.fetchall()
    heading = cur.description
    return render_template('test.html', headings = heading, form_data = formdata)


@app.route("/")
def home():
    # conn = psycopg2.connect(dbname="grofers", user="postgres", password="jatin", host="localhost", port="5432")
    # conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
    # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # cur.execute("create table users (username character varying not null, password character varying not null, refer_status bigint not null, refer_code character varying not null, referred_by character varying, grofers_cash bigint not null, primary key(username))")
    # cur.execute("insert into users2 (username, password, refer_status, refer_code, grofers_cash) values ('jatin', 'goyal', 0, 'jatin', 0)")
    # cur.execute("drop table if exists users")
    # cur.execute("create table referrals (referrer character varying not null, referee character varying not null, refer_count bigint not null, primary key(referrer, referee, refer_count))")
    # conn.commit()
    
    # cur.execute("select * from users")
    # formdata = cur.fetchall()
    # heading = cur.description
    # return render_template('test.html', headings = heading, form_data = formdata)
    return render_template('home.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/login-user", methods = ['POST', 'GET'])
def login_user():
    if request.method == 'GET':
        return f"The URL /login-user is accessed directly. Try going to '/login' to login"
    elif request.method == 'POST':
        # conn = psycopg2.connect(dbname="grofers", user="postgres", password="jatin", host="localhost", port="5432")
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("select * from users where username = %s and password = %s", (request.form['Username'], request.form['Password']))
        result = cur.rowcount
        formdata = cur.fetchall()
        if result > 0:
            if formdata[0][2] == 0:
                return render_template('login-user0.html',balance = formdata[0][5], name = request.form['Username'])
            else:
                return render_template('login-user1.html',balance = formdata[0][5], name = request.form['Username'])
        else:
            return render_template('invalid-login.html')

@app.route("/refer-code", methods = ['POST', 'GET'])
def refer_code():
    if request.method == 'GET':
        return f"The URL /refer-code is accessed directly. Try going to '/login' to login"
    elif request.method == 'POST':
        # conn = psycopg2.connect(dbname="grofers", user="postgres", password="jatin", host="localhost", port="5432")
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("update users set refer_status = 1 where username = %s", (request.form['Username'],))
        conn.commit()
        cur.execute("select * from users where username = %s", (request.form['Username'],))
        formdata = cur.fetchall()
        return render_template('refer-code.html',code = formdata[0][3], name = request.form['Username'])
        

@app.route("/withdraw-refer", methods = ['POST', 'GET'])
def withdraw_refer():
    if request.method == 'GET':
        return f"The URL /withdraw-refer is accessed directly. Try going to '/login' to login"
    elif request.method == 'POST':
        # conn = psycopg2.connect(dbname="grofers", user="postgres", password="jatin", host="localhost", port="5432")
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("update users set refer_status = 0 where username = %s", (request.form['Username'],))
        conn.commit()
        return render_template('withdraw-refer.html',name = request.form['Username'])

@app.route("/signup-user", methods = ['POST', 'GET'])
def signup_user():
    if request.method == 'GET':
        return f"The URL /signup-user is accessed directly. Try going to '/signup' to signup"
    elif request.method == 'POST':
        # conn = psycopg2.connect(dbname="grofers", user="postgres", password="jatin", host="localhost", port="5432")
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            if request.form['ReferralCode'] == '':
                def sha256_generator(str):
                    m = hashlib.sha256()
                    m.update(str.encode())
                    return m.hexdigest()
                refer_code = sha256_generator(request.form['Username'])[:5]
                # refer_code = request.form['Username']
                cur.execute("insert into users(username, password, refer_status, refer_code, grofers_cash) values (%s, %s, 0, %s, 0)", (request.form['Username'], request.form['Password'], refer_code))
                conn.commit()
            else:
                def sha256_generator(str):
                    m = hashlib.sha256()
                    m.update(str.encode())
                    return m.hexdigest()
                refer_code = sha256_generator(request.form['Username'])[:5]
                # refer_code = request.form['Username']
                cur.execute("select username from users where refer_status = 1 and refer_code = %s", (request.form['ReferralCode'],))
                formdata = cur.fetchall()
                if cur.rowcount > 0:
                    cur.execute("insert into users(username, password, refer_status, refer_code, referred_by, grofers_cash) values (%s, %s, 0, %s, %s, 100)", (request.form['Username'], request.form['Password'], refer_code, formdata[0][0]))
                    cur.execute("select * from referrals where referrer = %s", (formdata[0][0],))
                    refer_count = cur.rowcount + 1
                    referee = request.form['Username']
                    s = ''
                    for i in range(len(referee)-2):
                        s += '*'
                    referee = referee[0] + s + referee[-1]
                    cur.execute("insert into referrals(referrer, referee, refer_count) values (%s, %s, %s)", (formdata[0][0], referee, refer_count))
                    if refer_count == 3:
                        cur.execute("select referred_by from users where username = %s", (formdata[0][0],))
                        cash = 100
                        if cur.fetchall()[0][0] is not None:
                            cash += 100
                        cur.execute("update users set grofers_cash = %s where username = %s", (cash, formdata[0][0]))
                    elif refer_count >= 5:
                        cur.execute("select referred_by from users where username = %s", (formdata[0][0],))
                        cash = refer_count * 100
                        if cur.fetchall()[0][0] is not None:
                            cash += 100
                        cur.execute("update users set grofers_cash = %s where username = %s", (cash, formdata[0][0]))
                    conn.commit()
                else:
                    return render_template('invalid-signup.html')
            return render_template('signup-user.html')
        except:
            conn.rollback()
            return render_template('invalid-signup.html')

incentives = [0, 'Refer 2 more friends to earn ₹100', 'Refer 1 more friends to earn ₹100', '₹100', 'Refer 1 more friends to earn ₹400']

@app.route("/referral-history", methods = ['POST', 'GET'])
def referral_history():
    if request.method == 'GET':
        return f"The URL /referral-history is accessed directly. Try going to '/login' to login"
    elif request.method == 'POST':
        # conn = psycopg2.connect(dbname="grofers", user="postgres", password="jatin", host="localhost", port="5432")
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("select referee as \"Friends Referred\", refer_count as \"Incentive Earned\" from referrals where referrer = %s", (request.form['Username'],))
        formdata = cur.fetchall()
        heading = cur.description
        print(formdata)
        print(heading)
        for i in range(len(formdata)):
            ind = formdata[i][1]
            if ind > 4:
                formdata[i][1] = '₹100'
            else:
                formdata[i][1] = incentives[ind]
        print(formdata)
        print(heading)
        return render_template('test.html', form_data = formdata, headings = heading)

# app.run()