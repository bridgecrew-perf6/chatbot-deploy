from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from chat import get_response

app = Flask(__name__)
CORS(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)

@app.get("/")
def index_get():
    return render_template("base.html")

@app.route('/index', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        messages = request.get_json().get("message")
        #cursor = mysql.connection.cursor()
        #cursor.execute("INSERT INTO messages(messages) VALUES(%s)",[messages])
        #mysql.connection.commit()
        #cursor.close()
    return jsonify( {"answer": "Inserted Successfully"})
@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO messages(messages, response) VALUES(%s, %s)",[text, response])
    mysql.connection.commit()
    cursor.close()
    message = {"answer": response}
    return jsonify(message)
    
if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)