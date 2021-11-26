from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras

app = Flask(__name__)


@app.route("/admin")
def hello():
    conn = psycopg2.connect(dbname="grofers", user="postgres", password="jatin", host="localhost", port="5432")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("select * from users")
    formdata = cur.fetchall()
    heading = cur.description
    return render_template('test.html', headings = heading, form_data = formdata)


@app.route("/")
def admin():
    return render_template('admin.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/adminq", methods = ['POST', 'GET'])
def adminq():
    if request.method == 'GET':
        return f"The URL /adminq is accessed directly. Try going to '/login' to login"
    elif request.method == 'POST':
        conn = psycopg2.connect(dbname="grofers", user="postgres", password="jatin", host="localhost", port="5432")
        # conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("select * from users where username = %s and password = %s", (request.form['Username'], request.form['Password']))
        result = cur.rowcount
        if result > 0:
            return render_template('adminq.html',name = request.form['Username'])
        else:
            return render_template('invalid.html')

# app.run()