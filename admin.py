from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'flask'

app.secret_key = "super secret key"
mysql = MySQL(app)


@app.route("/")
def index():
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template('data_ad.html',username=session['username'])

@app.route("/login", methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM admin WHERE username=%s AND password=%s', (username,password))
        record = cursor.fetchone()
        if record:
            session['loggedin'] = True
            session['username'] = record[1]
            return redirect(url_for('select'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

@app.route("/select")
def select():
    cur = mysql.connection.cursor()
    cur.execute ("SELECT * FROM messages")

    rows=cur.fetchall()
    cur.close()
    return render_template('data_ad.html', rows=rows)

                           
if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5001)

