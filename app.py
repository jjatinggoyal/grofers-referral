from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras
import hashlib

app = Flask(__name__)

# a running build of this web-app can be accessed at grofers.onrender.com

# function to connect to db
# edit db credentials to connect to your db
def connect():
    conn = psycopg2.connect(dbname="grofers", user="postgres", password="jatin", host="localhost", port="5432")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return conn, cur

# generates referral code for a user by hashing their usesrname
def sha256_generator(str):
    m = hashlib.sha256()
    m.update(str.encode())
    return m.hexdigest()

# admin function for testing purpose. user does not need to know about this
# shows all registered users
@app.route("/admin")
def hello():
    conn, cur = connect()
    cur.execute("select * from users")
    formdata = cur.fetchall()
    heading = cur.description
    return render_template('test.html', headings = heading, form_data = formdata)

# home page. prompts the user to navigate to login or signup page
@app.route("/")
def home():
    return render_template('home.html')

# form to login
@app.route("/login")
def login():
    return render_template('login.html')

# form to signup
@app.route("/signup")
def signup():
    return render_template('signup.html')

# user dashboard on login
# prompts user to enroll for the referral program if not already
# once user has registered, the dashboard shows stats such as referral history, referral milestones 
# and a button to withdraw from the referral program
@app.route("/login-user", methods = ['POST', 'GET'])
def login_user():
    if request.method == 'GET':
        return f"The URL /login-user is accessed directly. Try going to '/login' to login"
    elif request.method == 'POST':
        
        conn, cur = connect()
        if 'bit' in request.form.keys():
            if request.form['bit'] == "1":
                cur.execute("select refer_code, grofers_cash from users where username = %s", (request.form['Username'],))
                dat = cur.fetchall()[0]
                return render_template('login-user1.html',balance = dat[1], name = request.form['Username'], code = dat[0])
            else:
                cur.execute("select grofers_cash from users where username = %s", (request.form['Username'],))
                dat = cur.fetchall()[0]
                return render_template('login-user0.html',balance = dat[0], name = request.form['Username'])
        cur.execute("select * from users where username = %s and password = %s", (request.form['Username'], request.form['Password']))
        result = cur.rowcount
        formdata = cur.fetchall()
        if result > 0:
            if formdata[0][2] == 0:
                return render_template('login-user0.html',balance = formdata[0][5], name = request.form['Username'])
            else:
                cur.execute("select refer_code from users where username = %s", (request.form['Username'],))
                return render_template('login-user1.html',balance = formdata[0][5], name = request.form['Username'], code = cur.fetchall()[0][0])
        else:
            return render_template('invalid-login.html')


# shows and activates referral code for a user when they enroll for the referral program on their dashboard
@app.route("/refer-code", methods = ['POST', 'GET'])
def refer_code():
    if request.method == 'GET':
        return f"The URL /refer-code is accessed directly. Try going to '/login' to login"
    elif request.method == 'POST':
        conn, cur = connect()
        cur.execute("update users set refer_status = 1 where username = %s", (request.form['Username'],))
        conn.commit()
        cur.execute("select * from users where username = %s", (request.form['Username'],))
        formdata = cur.fetchall()
        return render_template('refer-code.html',code = formdata[0][3], name = request.form['Username'])
        
# withdrawal from referral program. deactivates user's referral code
# the user dashboard now does not show options to view referral history and milestones
@app.route("/withdraw-refer", methods = ['POST', 'GET'])
def withdraw_refer():
    if request.method == 'GET':
        return f"The URL /withdraw-refer is accessed directly. Try going to '/login' to login"
    elif request.method == 'POST':
        conn, cur = connect()
        cur.execute("update users set refer_status = 0 where username = %s", (request.form['Username'],))
        conn.commit()
        return render_template('withdraw-refer.html',name = request.form['Username'])

# signup success/failure status page
# username and password can be any alphanumeric+special character string with at least 3 characters
# if a user joins through a valid refer code, they earn ₹100
# inserts and updates various datapoints
# a referral code is generated for each new user at signup, but it has to be activated by the user to be valid
# updates incentives for the referrer and referee
# updates referral history for referrer
@app.route("/signup-user", methods = ['POST', 'GET'])
def signup_user():
    if request.method == 'GET':
        return f"The URL /signup-user is accessed directly. Try going to '/signup' to signup"
    elif request.method == 'POST':
        if len(request.form['Username']) < 3 or len(request.form['Password']) < 3:
            err = 'username and password should have at least 3 letters'
            return render_template('invalid-signup.html', error = err)
        conn, cur = connect()
        try:
            if request.form['ReferralCode'] == '':
                refer_code = sha256_generator(request.form['Username'])[:5]
                cur.execute("insert into users(username, password, refer_status, refer_code, grofers_cash) values (%s, %s, 0, %s, 0)", (request.form['Username'], request.form['Password'], refer_code))
                conn.commit()
            else:
                refer_code = sha256_generator(request.form['Username'])[:5]
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
            return render_template('signup-user.html', name = request.form['Username'])
        except:
            conn.rollback()
            err = 'The user already exists or the referral code is invalid.'
            return render_template('invalid-signup.html', error = err)

# list to map incentives to number of referrals by a user
incentives = [0, 'Refer 2 more friends to earn ₹100', 'Refer 1 more friends to earn ₹100', '₹100', 'Refer 1 more friends to earn ₹400', '₹400']

# referral history of a user.
# fetches incentives earned on each referral
@app.route("/referral-history", methods = ['POST', 'GET'])
def referral_history():
    if request.method == 'GET':
        return f"The URL /referral-history is accessed directly. Try going to '/login' to login"
    elif request.method == 'POST':
        conn, cur = connect()
        cur.execute("select referee as \"Friends Referred\", refer_count as \"Incentive Earned\" from referrals where referrer = %s", (request.form['Username'],))
        formdata = cur.fetchall()
        heading = cur.description
        cur.execute("select username from users where username = %s", (request.form['Username'],))
        if len(formdata) == 0:
            return render_template('no-history.html', name = cur.fetchall()[0][0])
        for i in range(len(formdata)):
            ind = formdata[i][1]
            if ind > 5:
                formdata[i][1] = '₹100'
            else:
                formdata[i][1] = incentives[ind]
        
        return render_template('referral-history.html', name = cur.fetchall()[0][0], form_data = formdata, headings = heading)

# shows referral milestones - both completed and remaining for a user
@app.route("/referral-milestones", methods = ['POST', 'GET'])
def referral_milestones():
    if request.method == 'GET':
        return f"The URL /referral-milestones is accessed directly. Try going to '/login' to login"
    elif request.method == 'POST':
        conn, cur = connect()
        cur.execute("select referee as \"Friends Referred\", refer_count as \"Incentive Earned\" from referrals where referrer = %s", (request.form['Username'],))
        count = cur.rowcount
        one = two = three = 'Not completed'
        if count > 2 and count < 5:
            one = 'Completed'
        elif count == 5:
            one = two = 'Completed'
        elif count > 5:
            one = two = 'Completed'
            three = 'Keep Going for more!'
        cur.execute("select username from users where username = %s", (request.form['Username'],))
        return render_template('referral-milestones.html', name = cur.fetchall()[0][0], num = count, one = one, two = two, three = three)

# app.run()